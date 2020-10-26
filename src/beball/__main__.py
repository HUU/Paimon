#!/usr/bin/env python3.7

import daemon
import lockfile
import logging
import signal
import sys
import time

from typing import Optional
from multiprocessing import Queue, Event, synchronize
from .conductor import Conductor
from .watcher import StreamSegmentWatcher
from .uploader import VeryDeterminedUploader


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class BeballDaemon:

    upload_queue: Optional[Queue] = None
    shutdown_uploader: Optional[synchronize.Event] = None
    conductor: Optional[Conductor] = None
    watcher: Optional[StreamSegmentWatcher] = None
    uploader: Optional[VeryDeterminedUploader] = None

    def sigterm(self, signum, frame):
        self.cleanup()

    def cleanup(self):
        logging.info("Beball: exiting cleanly...")
        if self.watcher:
            self.watcher.stop()
            self.watcher = None
        if self.shutdown_uploader:
            self.shutdown_uploader.set()
            self.shutdown_uploader = None
        if self.upload_queue:
            self.upload_queue.close()
            self.upload_queue = None
        if self.uploader:
            self.uploader.join(10)
            if self.uploader.is_alive():
                self.uploader.terminate()
            self.uploader = None
        logging.info("Beball: done.")

    def start(self):
        logging.info("Beball: starting...")
        self.upload_queue = Queue()
        self.shutdown_uploader = Event()
        self.conductor = Conductor(self.upload_queue)
        self.watcher = StreamSegmentWatcher("/tmp/hls", self.conductor)
        self.uploader = VeryDeterminedUploader(
            self.upload_queue, self.shutdown_uploader
        )

        self.watcher.start()
        self.uploader.start()
        logging.info("Beball: started.")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            self.cleanup()


if __name__ == "__main__":
    logging.debug("Beball: daemonizing...")
    beball = BeballDaemon()
    with daemon.DaemonContext(
        stdout=sys.stdout,
        stderr=sys.stderr,
        detach_process=False,
        umask=0o002,
        pidfile=lockfile.FileLock("/var/run/beball.pid"),
        signal_map={
            signal.SIGTERM: beball.sigterm,
            signal.SIGHUP: "terminate",
        },
    ):
        beball.start()
