#!/usr/bin/env python3.7

import daemon
import lockfile
import signal
import sys
import time

from .conductor import Conductor
from .watcher import StreamSegmentWatcher

conductor = Conductor()
watcher = StreamSegmentWatcher("/tmp/hls", conductor)


def cleanup():
    watcher.stop()


def start():
    print("daemonizing")
    with daemon.DaemonContext(
        stdout=sys.stdout,
        stderr=sys.stderr,
        detach_process=False,
        umask=0o002,
        pidfile=lockfile.FileLock("/var/run/beball.pid"),
        signal_map={
            signal.SIGTERM: cleanup,
            signal.SIGHUP: "terminate",
        },
    ):
        print("starting")
        watcher.start()

        while True:
            time.sleep(60)


if __name__ == "__main__":
    start()
