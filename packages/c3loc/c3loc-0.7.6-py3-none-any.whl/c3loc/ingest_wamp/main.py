#!/bin/env python
"""Reference Implementation of v1 C3 Security Beacon Auth Server."""
import asyncio
import os
import signal

from autobahn.asyncio.wamp import ApplicationRunner
import click
try:
    import uvloop  # type: ignore
    uvloop.install()
except ImportError:
    pass

from ..config import CONFIG
from ..db import init_db_pool
import c3loc.stats as stats
from .wamp import WampHandler

def default_handler(loop, context):
    print(f"Unhandled exception: {context['message']}", context)
    loop.stop()


@click.command()
@click.option('--realm', '-r', default="realm1")
def main(realm: str) -> None:
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(default_handler)
    if signal is not None and os.name != 'nt':
        loop.add_signal_handler(signal.SIGINT, loop.stop)

    db_pool = loop.run_until_complete(init_db_pool('ingest_wamp'))
    WampHandler.db_pool = db_pool

    stats.run(CONFIG['STATS_INTERVAL'])

    runner = ApplicationRunner(CONFIG['WAMP_URI'], realm)
    runner.run(WampHandler)


if __name__ == '__main__':
    main()
