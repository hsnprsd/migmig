import asyncio

from lib.inbounds.socks5 import Socks5Inbound
from lib.outbounds.migmig import MigmigOutbound


async def main():
    inbound_host = "127.0.0.1"
    inbound_port = 1080

    outbound_host = "127.0.0.1"
    outbound_port = 8080

    outbound = MigmigOutbound(outbound_host, outbound_port)

    inbound = Socks5Inbound(inbound_host, inbound_port, outbound=outbound)
    await inbound.start()


if __name__ == "__main__":
    asyncio.run(main())
