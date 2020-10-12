#!/usr/bin/env python3.7

import daemon
import lockfile
import signal
import sys

from .conductor import Conductor
from .watcher import StreamSegmentWatcher

conductor = Conductor()
watcher = StreamSegmentWatcher("/tmp/hls", conductor)


def cleanup():
    watcher.stop()


def start():
    with daemon.DaemonContext(
        stdout=sys.stdout,
        stderr=sys.stderr,
        umask=0o002,
        pidfile=lockfile.FileLock("/var/run/beball.pid"),
        signal_map={
            signal.SIGTERM: cleanup,
            signal.SIGHUP: "terminate",
        },
    ):
        watcher.start()


if __name__ == "__main__":
    start()
