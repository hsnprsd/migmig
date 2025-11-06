import asyncio

from lib.proxy import ConnectionRequest, forward


class DirectOutbound:
    async def outbound(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        connection_request: ConnectionRequest,
    ) -> None:
        print(
            "direct outbound connection to",
            connection_request.host,
            connection_request.port,
        )

        remote_reader, remote_writer = await asyncio.open_connection(
            connection_request.host, connection_request.port
        )

        await asyncio.gather(
            forward(reader, remote_writer),
            forward(remote_reader, writer),
        )
