# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

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
# SOFTWARE
"""The V4 Voice Gateway Impl"""

import asyncio
import json
import logging
import struct
import time
from random import random

import aiohttp

from ..state import ConnectionState
from ..utils import create_snowflake

_log = logging.getLogger(__name__)


class VoiceGateway:
    def __init__(self, state: ConnectionState, guild_id: int, hook):
        self.state = state
        self.hook = hook
        self.server_id = guild_id
        self.session_id: int = None
        self.secret_key: str = None
        self.kept_alive: bool = False
        self.ws: aiohttp.ClientWebSocketResponse = None

    async def hook(self, *args):
        pass

    def update_session_id(self, id: int):
        self.session_id = id

    async def send_json(self, payload: dict):
        _log.debug("Sending payload data %s via the voice gateway", payload)
        await self.ws.send_str(json.dumps(payload))

    async def resume(self):
        payload = {
            "op": 7,
            "d": {
                "token": self.state.app.token,
                "server_id": str(self.server_id),
                "session_id": self.client.session_id,
            },
        }
        await self.send_json(payload)

    async def identify(self):
        payload = {
            "op": 0,
            "d": {
                "server_id": str(self.server_id),
                "user_id": self.state.app.user.id,
                "session_id": self.client.session_id,
                "token": self.state.app.token,
            },
        }
        await self.send_json(payload)

    async def connect(self, resume: bool = False):
        self.ws = await self.client._state.app.factory.ws_connect(
            self.gateway, compress=15
        )

        if not resume:
            await self.identify()
            self.client._state.loop.create_task(self.recv())
        else:
            await self.resume()
            self.client.start.loop.create_task(self.recv())

    # i know this is a loss of customization here but doing this makes,
    # the development experience so much easier and since i wouldn't guess people are customizing here
    # it's ok.
    @classmethod
    async def voice_client_entry(cls, client, *, hook=None):
        gateway = "wss://" + client.endpoint + "/?v=4"
        self = cls(client._state, client.guild_id, hook=hook)
        self.gateway = gateway
        self.client = client

        return self

    async def select_protocol(self, ip, port, mode):
        payload = {
            "op": 1,
            "d": {
                "protocol": "udp",
                "data": {
                    "address": ip,
                    "port": port,
                    "mode": mode,
                },
            },
        }
        await self.send_json(payload)

    async def client_connect(self):
        payload = {"op": 12, "d": {"audio_ssrc": self.client.ssrc}}
        await self.send_json(payload)

    async def speak(self, state=1):
        payload = {
            "op": 5,
            "d": {
                "speaking": int(state),
                "delay": 0,
            },
        }
        await self.send_json(payload)

    async def recv(self):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                op: int = data["op"]
                d: dict = data["d"]
                _log.debug("> %s", data)

                if op == 2:
                    await self.ready(d)

                elif op == 6:
                    self.kept_alive = True
                    _log.debug("> %s, kept the connection alive", d)

                elif op == 9:
                    _log.info("Resumed connection successfully")

                elif op == 4:
                    _log.info("Received session description")
                    self.client.mode = d["mode"]
                    self.secret_key = self.client.secret_key = d.get("secret_key")
                    await self.speak()
                    await self.speak(False)

                elif op == 8:
                    interval: int = d["heartbeat_interval"] / 1000
                    await self.hello(interval=interval)

    async def heartbeat(self, interval: float):
        while not self.ws.closed:
            if not self.kept_alive:
                await self.close(1008)
                await self.connect(resume=True)
            self.kept_alive = False
            await self.send_json({"op": 3, "d": create_snowflake()})
            await asyncio.sleep(interval)

    async def ready(self, data: dict):
        client = self.client
        client.ssrc = data["ssrc"]
        client.voice_port = data["port"]
        client.endpoint_ip = data["ip"]

        packet = bytearray(70)
        struct.pack_into(">H", packet, 0, 1)
        struct.pack_into(">H", packet, 2, 70)
        struct.pack_into(">I", packet, 4, client.ssrc)
        client.socket.sendto(packet, (client.endpoint_ip, client.voice_port))
        recv = self.state.loop.sock_recv(client.socket, 70)
        _log.debug("Received initial connection: %s", recv)

        ip_end = recv.index(0, 4)
        client.ip = recv[4:ip_end].decode("ascii")

        client.port = struct.unpack_from(">H", recv, len(recv) - 2)
        _log.debug("IP was detected: %s, port: %s", client.ip, client.port)

        modes = [mode for mode in data["modes"] if mode in self.client.supported_modes]
        _log.debug("Using following encryption mode(s): %s", modes)

        mode = modes[0]
        await self.select_protocol(client.ip, client.port, mode)
        _log.info("Using voice protocol: %s", mode)

    async def hello(self, interval: float):
        init = interval * random()
        await asyncio.sleep(init)
        self.kept_alive = (
            True  # exception to not kill the connection when saying hello.
        )
        await self.heartbeat(interval)

    async def close(self, code: int):
        await self.ws.close(code=code)
