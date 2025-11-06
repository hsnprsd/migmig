import asyncio
import ssl
from typing import Optional

from lib.http import read_http_request_header
from lib.inbounds.inbound import Inbound
from lib.outbounds.outbound import Outbound
from lib.proxy import ConnectionRequest
from lib.tls import ServerTLSConfig


class MigmigInbound(Inbound):
    def __init__(
        self,
        host: str,
        port: int,
        outbound: Outbound,
        tls: Optional[ServerTLSConfig] = None,
    ) -> None:
        super().__init__(outbound)
        self.host = host
        self.port = port
        self.ssl_context = None

        if tls:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(tls.cert_file, tls.key_file)

    async def start(self) -> None:
        server = await asyncio.start_server(
            self.inbound,
            self.host,
            self.port,
            ssl=self.ssl_context,
        )

        print("migmig inbound server started on", self.host, self.port)
        if self.ssl_context:
            print("migmig inbound server using TLS")

        async with server:
            await server.serve_forever()

    async def inbound(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        print("migmig inbound connection from:", writer.get_extra_info("peername"))

        await read_http_request_header(reader)

        connection_request = await ConnectionRequest.read_from(reader)

        writer.write(b"HTTP/1.1 200 OK\r\n\r\n")
        await writer.drain()

        await self.outbound.outbound(reader, writer, connection_request)
