import asyncio
from dataclasses import dataclass

SEPARATOR = b"\r\n\r\n"


@dataclass
class HTTPRequestHeader:
    method: str
    path: str
    version: str
    headers: dict[str, str]


@dataclass
class HTTPResponseHeader:
    version: str
    status: str
    headers: dict[str, str]


async def read_http_response_header(
    reader: asyncio.StreamReader,
) -> HTTPResponseHeader:
    buf = await reader.readuntil(SEPARATOR)

    lines = buf.split(b"\r\n")

    version, status = tuple(lines[0].split(b" ", 1))

    headers = {}
    for line in lines[1:]:
        if line:
            header_name, header_value = tuple(line.split(b": "))
            headers[header_name.decode("utf-8")] = header_value.decode("utf-8")

    return HTTPResponseHeader(
        version=version.decode("utf-8"),
        status=status.decode("utf-8"),
        headers=headers,
    )


async def read_http_request_header(
    reader: asyncio.StreamReader,
) -> HTTPRequestHeader:
    buf = await reader.readuntil(SEPARATOR)

    lines = buf.split(b"\r\n")

    method, path, version = tuple(lines[0].split(b" "))

    headers = {}
    for line in lines[1:]:
        if line:
            header_name, header_value = tuple(line.split(b": "))
            headers[header_name.decode("utf-8")] = header_value.decode("utf-8")

    return HTTPRequestHeader(
        method=method.decode("utf-8"),
        path=path.decode("utf-8"),
        version=version.decode("utf-8"),
        headers=headers,
    )
