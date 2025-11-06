import asyncio
import socket
import struct

from lib.outbounds.outbound import Outbound
from lib.proxy import ConnectionRequest

SOCKS_VERSION = 0x05

AUTH_METHOD_NO_AUTH = 0x00

CMD_ESTABLISH_TCP_CONNECTION = 0x01

ADDR_TYPE_IPV4 = 0x01
ADDR_TYPE_DOMAIN = 0x03
ADDR_TYPE_IPV6 = 0x04

STATUS_REQUEST_GRANTED = 0x00
STATUS_GENERAL_FAILURE = 0x01


class Socks5Inbound:
    def __init__(self, host: str, port: int, outbound: Outbound) -> None:
        self.host = host
        self.port = port
        self.outbound = outbound

    async def start(self) -> None:
        server = await asyncio.start_server(self.inbound, self.host, self.port)
        async with server:
            await server.serve_forever()

    async def inbound(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> ConnectionRequest:
        print("socks5 inbound connection from:", writer.get_extra_info("peername"))

        header = await reader.readexactly(2)
        version, nauth = header[0], header[1]

        if version != SOCKS_VERSION:
            print("invalid socks version:", version)
            writer.close()
            await writer.wait_closed()
            return

        cauth = None
        auth_methods = await reader.readexactly(nauth)
        for i, auth_method in enumerate(auth_methods):
            if auth_method == AUTH_METHOD_NO_AUTH:
                cauth = i
                break
        else:
            print("invalid auth method:", auth_methods)
            writer.close()
            await writer.wait_closed()
            return

        writer.write(struct.pack("BB", SOCKS_VERSION, cauth))
        await writer.drain()

        version, cmd, _, addr_type = await reader.readexactly(4)

        if version != SOCKS_VERSION:
            writer.close()
            await writer.wait_closed()
            return

        if cmd != CMD_ESTABLISH_TCP_CONNECTION:
            writer.close()
            await writer.wait_closed()
            return

        if addr_type == ADDR_TYPE_IPV4:
            addr = await reader.readexactly(4)
            port = await reader.readexactly(2)
            addr = socket.inet_ntop(socket.AF_INET, addr)
        elif addr_type == ADDR_TYPE_DOMAIN:
            addr_len = await reader.readexactly(1)
            addr = await reader.readexactly(addr_len[0])
            port = await reader.readexactly(2)
            addr = addr.decode("utf-8")
        elif addr_type == ADDR_TYPE_IPV6:
            addr = await reader.readexactly(16)
            port = await reader.readexactly(2)
            addr = socket.inet_ntop(socket.AF_INET6, addr)
        else:
            writer.close()
            await writer.wait_closed()
            return

        port = int.from_bytes(port, "big")

        writer.write(
            struct.pack(
                "BBBBBBBBBB",
                SOCKS_VERSION,
                STATUS_REQUEST_GRANTED,
                0x00,
                ADDR_TYPE_IPV4,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            )
        )
        await writer.drain()

        connection_request = ConnectionRequest(host=addr, port=port)

        await self.outbound.outbound(reader, writer, connection_request)
