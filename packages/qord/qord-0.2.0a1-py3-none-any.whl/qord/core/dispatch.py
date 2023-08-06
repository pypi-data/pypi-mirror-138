# MIT License

# Copyright (c) 2022 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from qord.models.users import ClientUser
from qord.models.guilds import Guild
from qord import events

import asyncio
import copy
import inspect
import logging
import typing

if typing.TYPE_CHECKING:
    from qord.core.client import Client
    from qord.core.shard import Shard


def event_dispatch_handler(name: str):
    def _wrap(func: typing.Callable[[DispatchHandler, Shard, typing.Any], typing.Any]):
        func.__handler_event__ = name
        return func

    return _wrap


class DispatchHandler:
    r"""Internal class that handles gateway events dispatches."""

    def __init__(self, client: Client, ready_timeout: float = 2.0, debug_events: bool = False) -> None:
        self.client = client
        self.ready_timeout = ready_timeout
        self.debug_events = debug_events
        self.cache = client._cache
        self._invoke = client.invoke_event
        self._shards_connected = asyncio.Event()
        self._shards_ready = asyncio.Event()
        self._guild_create_waiter = None
        self._ready_task = None
        self._update_handlers()

    def _update_handlers(self):
        self._handlers = {}
        members = inspect.getmembers(self)

        for _, member in members:
            try:
                self._handlers[member.__handler_event__] = member
            except AttributeError:
                pass

    def invoke(self, event: events.BaseEvent) -> None:
        self._invoke(event.event_name, event)

    async def handle(self, shard: Shard, title: str, data: typing.Any) -> None:
        if self.debug_events:
            event = events.GatewayDispatch(shard=shard, title=title, data=data)
            self.invoke(event)

        try:
            handler = self._handlers[title]
        except KeyError:
            return
        else:
            await handler(shard, data)

    async def _prepare_ready(self, shard: typing.Optional[Shard] = None):
        # Setting a timeout for GUILD_CREATE to allow the given shards
        # to lazy load the guilds before dispatching ready event.
        timeout = self.ready_timeout

        if shard is None:
            # shard being None means we are waiting for all shards to lazy load the
            # guilds so wait for all the shards to connect first.
            await self._shards_connected.wait()

        while True:
            self._guild_create_waiter = asyncio.Future()
            try:
                await asyncio.wait_for(self._guild_create_waiter, timeout=timeout)
            except asyncio.TimeoutError:
                break

        # Do some cleanup and invoke the ready event
        self._guild_create_waiter = None
        event = events.Ready() if shard is None else events.ShardReady(shard=shard)
        self.invoke(event)

        if shard is None:
            self._shards_ready.set()
            self._ready_task = None

    @event_dispatch_handler("READY")
    async def on_ready(self, shard: Shard, data: typing.Any) -> None:
        user = ClientUser(data["user"], client=self.client)
        self.cache.add_user(user)
        self.client._user = user

        shard._log(logging.INFO, "Lazy loading cache for ~%s guilds in background." % len(data["guilds"]))

        # Wait for current shard to backfill guilds.
        coro = self._prepare_ready(shard)
        asyncio.create_task(coro)

        if self._ready_task is None:
            # Wait for all shards to backfill guilds in background.
            coro = self._prepare_ready()
            self._ready_task = asyncio.create_task(coro)

    @event_dispatch_handler("GUILD_CREATE")
    async def on_guild_create(self, shard: Shard, data: typing.Any) -> None:
        unavailable = data.get("unavailable")

        if unavailable is True:
            # TODO: Not sure about what to do about joining an unavailable
            # guild but for now, Do nothing
            return

        guild = Guild(data, client=self.client, enable_cache=True)
        self.cache.add_guild(guild)

        # Notify waiters for dispatching ready event
        waiter = self._guild_create_waiter

        if waiter and not waiter.done():
            waiter.set_result(guild)

        # unavailable being False means that an unavailable guild
        # either because of outage or from READY event has became available.
        # And unavailable not being included in payload
        # means that bot has joined a new guild.
        # https://github.com/discord/discord-api-docs/issues/4518
        if unavailable is False:
            event = events.GuildAvailable(guild=guild, shard=shard)
        elif unavailable is None:
            event = events.GuildJoin(guild=guild, shard=shard)

        self.invoke(event) # type: ignore

    @event_dispatch_handler("GUILD_UPDATE")
    async def on_guild_update(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_UPDATE: Unknown guild with ID %s", guild_id)
            return

        before = copy.copy(guild)
        guild._update_with_data(data)

        event = events.GuildUpdate(before=before, after=guild, shard=shard)
        self.invoke(event)

    @event_dispatch_handler("GUILD_DELETE")
    async def on_guild_delete(self, shard: Shard, data: typing.Any) -> None:
        guild_id = int(data["id"])
        guild = self.cache.get_guild(guild_id)

        if guild is None:
            shard._log(logging.DEBUG, "GUILD_DELETE: Unknown guild with ID %s", guild_id)
            return

        unavailable = data.get("unavailable")

        if unavailable is None:
            # Bot is removed from the guild.
            guild = self.cache.delete_guild(guild_id)
            if guild is None:
                # already removed?
                return
            event = events.GuildLeave(shard=shard, guild=guild)
        else:
            # Guild became unavailable due to an outage
            # TODO: Evict guild here?
            guild.unavailable = True
            event = events.GuildUnavailable(shard=shard, guild=guild)

        self.invoke(event)