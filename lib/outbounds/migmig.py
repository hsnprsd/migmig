import asyncio
import ssl
from typing import Optional

from lib.http import read_http_response_header
from lib.outbounds.outbound import Outbound
from lib.proxy import ConnectionRequest, forward
from lib.tls import ClientTLSConfig


class MigmigOutbound(Outbound):
    def __init__(
        self,
        server_host: str,
        server_port: int,
        tls: Optional[ClientTLSConfig] = None,
    ) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.ssl_context = None

        if tls:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            if not tls.verify:
                self.ssl_context.check_hostname = False
                self.ssl_context.verify_mode = ssl.CERT_NONE

    async def outbound(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        connection_request: ConnectionRequest,
    ) -> None:
        print(
            "migmig outbound connection to:",
            connection_request.host,
            connection_request.port,
        )

        remote_reader, remote_writer = await asyncio.open_connection(
            self.server_host,
            self.server_port,
            ssl=self.ssl_context,
        )

        remote_writer.write(
            f"GET / HTTP/1.1\r\nHost: {self.server_host}\r\n\r\n".encode("utf-8")
        )
        remote_writer.write(connection_request.to_bytes())
        await remote_writer.drain()

        response_header = await read_http_response_header(remote_reader)
        if response_header.status != "200 OK":
            writer.close()
            await writer.wait_closed()
            return

        await asyncio.gather(
            forward(reader, remote_writer),
            forward(remote_reader, writer),
        )
