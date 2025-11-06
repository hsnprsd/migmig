import asyncio
from dataclasses import dataclass
from typing import Optional


@dataclass
class HTTPRequestHeader:
    method: str
    path: str
    version: str
    headers: dict[str, str]


@dataclass
class HTTPResponseHeader:
    status: str
    version: str
    headers: dict[str, str]


async def read_http_response_header(
    reader: asyncio.StreamReader,
) -> tuple[Optional[HTTPResponseHeader], bytes]:
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = await reader.read(4096)
        if not chunk:
            return None, buf
        buf += chunk

    response_header = buf[: buf.find(b"\r\n\r\n")]
    buf = buf[buf.find(b"\r\n\r\n") + len(b"\r\n\r\n") :]

    response_header_lines = response_header.split(b"\r\n")

    response_line = response_header_lines[0]
    version, status = tuple(response_line.split(b" ", 1))

    headers = {}
    for line in response_header_lines[1:]:
        header_name, header_value = tuple(line.split(b": "))
        headers[header_name.decode("utf-8")] = header_value.decode("utf-8")

    return (
        HTTPResponseHeader(
            status=status.decode("utf-8"),
            version=version.decode("utf-8"),
            headers=headers,
        ),
        buf,
    )


async def read_http_request_header(
    reader: asyncio.StreamReader,
) -> tuple[Optional[HTTPRequestHeader], bytes]:
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = await reader.read(4096)
        if not chunk:
            return None, buf
        buf += chunk

    request_header, extra = tuple(buf.split(b"\r\n\r\n", 1))

    request_line, headers_block = tuple(request_header.split(b"\r\n", 1))
    method, path, version = tuple(request_line.split(b" "))

    headers = {}
    for line in headers_block.split(b"\r\n"):
        if line:
            header_name, header_value = tuple(line.split(b": "))
            headers[header_name.decode("utf-8")] = header_value.decode("utf-8")

    return (
        HTTPRequestHeader(
            method=method.decode("utf-8"),
            path=path.decode("utf-8"),
            version=version.decode("utf-8"),
            headers=headers,
        ),
        extra,
    )
