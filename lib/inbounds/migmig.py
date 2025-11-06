import asyncio

from lib.http import read_http_request_header
from lib.inbounds.inbound import Inbound
from lib.outbounds.outbound import Outbound
from lib.proxy import ConnectionRequest


class MigmigInbound(Inbound):
    def __init__(self, host: str, port: int, outbound: Outbound) -> None:
        super().__init__(outbound)
        self.host = host
        self.port = port

    async def start(self) -> None:
        server = await asyncio.start_server(self.inbound, self.host, self.port)
        async with server:
            await server.serve_forever()

    async def inbound(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        print("migmig inbound connection from:", writer.get_extra_info("peername"))

        _, request_body = await read_http_request_header(reader)

        connection_request = ConnectionRequest.from_bytes(request_body)

        writer.write(b"HTTP/1.1 200 OK\r\n\r\n")
        await writer.drain()

        await self.outbound.outbound(reader, writer, connection_request)
