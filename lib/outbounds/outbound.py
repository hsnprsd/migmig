import asyncio

from lib.proxy import ConnectionRequest


class Outbound:
    async def outbound(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        connection_request: ConnectionRequest,
    ) -> None:
        raise NotImplementedError
