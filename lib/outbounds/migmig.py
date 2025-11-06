import asyncio

from lib.http import read_http_response_header
from lib.outbounds.outbound import Outbound
from lib.proxy import ConnectionRequest, forward


class MigmigOutbound(Outbound):
    def __init__(self, server_host: str, server_port: int) -> None:
        self.server_host = server_host
        self.server_port = server_port

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
            self.server_host, self.server_port
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
