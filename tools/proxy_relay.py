#!/usr/bin/env python3
"""Route proxy-unaware clients (Modal's gRPC client) through HTTPS_PROXY.

Some sandboxes (e.g. Claude Code cloud sessions) only allow outbound HTTPS via
an HTTP CONNECT proxy in HTTPS_PROXY, and have no direct DNS. Modal's client
ignores HTTPS_PROXY and fails with "Could not connect to the Modal server"
(DEBUG log: "Name or service not known"). This tool:

  1. maps the given hosts to 127.0.0.1 in /etc/hosts (needs root), and
  2. listens on 127.0.0.1:443, reads the TLS SNI of each connection and tunnels
     it to <host>:443 with CONNECT through HTTPS_PROXY.

Traffic still goes through the proxy, so its allow-list and TLS inspection
apply unchanged; the client must trust the proxy's CA (SSL_CERT_FILE).

Usage (toolkit root):
    uv run tools/proxy_relay.py --check                     # is it needed / running?
    nohup uv run tools/proxy_relay.py > /tmp/proxy_relay.log 2>&1 &
    uv run tools/proxy_relay.py --host api.modal.com --host other.example.com

Then run Modal as usual, e.g. `uv run modal app list`.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import socket
import sys
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_HOSTS = ["api.modal.com"]
HOSTS_FILE = Path("/etc/hosts")
MARK = "# proxy_relay"


def parse_sni(data: bytes) -> str | None:
    """Server name from a TLS ClientHello, or None."""
    try:
        p = 5 + 4 + 2 + 32                                   # record + handshake hdr, version, random
        p += 1 + data[p]                                     # session id
        p += 2 + int.from_bytes(data[p:p + 2], "big")        # cipher suites
        p += 1 + data[p]                                     # compression methods
        end = p + 2 + int.from_bytes(data[p:p + 2], "big")
        p += 2
        while p < end:
            ext_type = int.from_bytes(data[p:p + 2], "big")
            ext_len = int.from_bytes(data[p + 2:p + 4], "big")
            if ext_type == 0:                                # server_name
                n = int.from_bytes(data[p + 7:p + 9], "big")
                return data[p + 9:p + 9 + n].decode()
            p += 4 + ext_len
    except (IndexError, UnicodeDecodeError):
        pass
    return None


def map_hosts(hosts: list[str]) -> None:
    lines = HOSTS_FILE.read_text().splitlines()
    present = {ln.split()[1] for ln in lines if ln.strip() and not ln.startswith("#")
               and len(ln.split()) > 1 and ln.split()[0] == "127.0.0.1"}
    missing = [h for h in hosts if h not in present]
    if missing:
        with HOSTS_FILE.open("a") as f:
            for h in missing:
                f.write(f"127.0.0.1 {h} {MARK}\n")
        print(f"mapped to 127.0.0.1 in /etc/hosts: {', '.join(missing)}", flush=True)


async def pipe(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        while chunk := await reader.read(65536):
            writer.write(chunk)
            await writer.drain()
    except (ConnectionError, asyncio.IncompleteReadError):
        pass
    finally:
        writer.close()


def make_handler(proxy, allowed: set[str]):
    async def handle(cr: asyncio.StreamReader, cw: asyncio.StreamWriter) -> None:
        first = await cr.read(65536)
        host = parse_sni(first)
        if host not in allowed:
            print(f"rejected connection for SNI {host!r}", flush=True)
            cw.close()
            return
        pr, pw = await asyncio.open_connection(proxy.hostname, proxy.port)
        pw.write(f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}:443\r\n\r\n".encode())
        await pw.drain()
        head = await pr.readuntil(b"\r\n\r\n")
        status = head.split(b"\r\n", 1)[0]
        if b" 200" not in status:
            print(f"proxy refused {host}: {status.decode(errors='replace')}", flush=True)
            cw.close()
            pw.close()
            return
        pw.write(first)
        await pw.drain()
        await asyncio.gather(pipe(cr, pw), pipe(pr, cw))
    return handle


def relay_running() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", 443), timeout=1):
            return True
    except OSError:
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--host", action="append", help=f"host to relay (default: {DEFAULT_HOSTS})")
    ap.add_argument("--check", action="store_true", help="report whether the relay is needed/running")
    args = ap.parse_args()
    hosts = args.host or DEFAULT_HOSTS

    proxy_url = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if args.check:
        print(f"HTTPS_PROXY: {'set' if proxy_url else 'not set (relay not needed)'}")
        print(f"relay listening on 127.0.0.1:443: {relay_running()}")
        for h in hosts:
            try:
                print(f"{h} resolves to {socket.gethostbyname(h)}")
            except OSError:
                print(f"{h} does not resolve (start the relay)")
        return
    if not proxy_url:
        sys.exit("HTTPS_PROXY is not set — connect directly, no relay needed.")
    if relay_running():
        sys.exit("Something is already listening on 127.0.0.1:443 (relay already running?).")
    if os.geteuid() != 0:
        sys.exit("Needs root: it edits /etc/hosts and binds port 443.")

    map_hosts(hosts)
    proxy = urlparse(proxy_url)

    async def serve() -> None:
        server = await asyncio.start_server(make_handler(proxy, set(hosts)), "127.0.0.1", 443)
        print(f"relay up on 127.0.0.1:443 for {', '.join(hosts)} via {proxy.hostname}:{proxy.port}",
              flush=True)
        async with server:
            await server.serve_forever()

    asyncio.run(serve())


if __name__ == "__main__":
    main()
