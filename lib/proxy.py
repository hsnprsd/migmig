import asyncio
import struct
from dataclasses import dataclass


@dataclass
class ConnectionRequest:
    host: str
    port: int

    def to_bytes(self) -> bytes:
        host_bytes = self.host.encode("utf-8")
        return (
            struct.pack("B", len(host_bytes)) + host_bytes + struct.pack("H", self.port)
        )

    @staticmethod
    async def read_from(reader: asyncio.StreamReader) -> "ConnectionRequest":
        host_len = await reader.readexactly(1)
        host = await reader.readexactly(host_len[0])
        port = struct.unpack("H", await reader.readexactly(2))[0]
        return ConnectionRequest(host=host.decode("utf-8"), port=port)


async def forward(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while True:
            chunk = await reader.read(4096)
            if not chunk:
                break
            writer.write(chunk)
            await writer.drain()
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass
        writer.close()
        await writer.wait_closed()
