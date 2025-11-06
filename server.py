import argparse
import asyncio

from lib.inbounds.migmig import MigmigInbound
from lib.outbounds.direct import DirectOutbound
from lib.tls import ServerTLSConfig


async def server():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", help="Inbound listen host")
    parser.add_argument("--port", type=int, default=8443, help="Inbound listen port")
    parser.add_argument(
        "--cert-file", type=str, default=None, help="TLS certificate file (optional)"
    )
    parser.add_argument(
        "--key-file", type=str, default=None, help="TLS key file (optional)"
    )
    args = parser.parse_args()

    inbound_host = args.host
    inbound_port = args.port

    outbound = DirectOutbound()

    if args.cert_file and args.key_file:
        tls = ServerTLSConfig(cert_file=args.cert_file, key_file=args.key_file)
    else:
        tls = None

    inbound = MigmigInbound(
        inbound_host,
        inbound_port,
        tls=tls,
        outbound=outbound,
    )

    await inbound.start()


if __name__ == "__main__":
    asyncio.run(server())
