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
    def from_bytes(bytes: bytes) -> "ConnectionRequest":
        host_len = bytes[0]
        host = bytes[1 : 1 + host_len].decode("utf-8")
        port = struct.unpack("H", bytes[1 + host_len :])[0]
        return ConnectionRequest(host=host, port=port)


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
