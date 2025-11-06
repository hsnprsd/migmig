from dataclasses import dataclass
from typing import Optional


@dataclass
class ServerTLSConfig:
    cert_file: str
    key_file: str


@dataclass
class ClientTLSConfig:
    verify: bool = True
