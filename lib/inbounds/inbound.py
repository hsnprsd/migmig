from lib.outbounds.outbound import Outbound


class Inbound:
    def __init__(self, outbound: Outbound) -> None:
        self.outbound = outbound

    async def start(self) -> None:
        raise NotImplementedError
