import asyncio

from lib.inbounds.migmig import MigmigInbound
from lib.outbounds.direct import DirectOutbound
from lib.tls import ServerTLSConfig


async def server():
    inbound_host = "127.0.0.1"
    inbound_port = 8080

    outbound = DirectOutbound()

    inbound = MigmigInbound(
        inbound_host,
        inbound_port,
        tls=ServerTLSConfig(cert_file="server.crt", key_file="server.key"),
        outbound=outbound,
    )

    await inbound.start()


if __name__ == "__main__":
    asyncio.run(server())
