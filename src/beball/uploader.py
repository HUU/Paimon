from multiprocessing import Process, Queue, synchronize

import queue
import logging

LOGGER = logging.getLogger(__name__)


class VeryDeterminedUploader(Process):
    def __init__(self, upload_queue: Queue, shutdown_event: synchronize.Event):
        super(Process, self).__init__()
        self.__upload_queue = upload_queue
        self.__shutdown_event = shutdown_event

    def run(self):
        LOGGER.info("Uploader process is starting...")

        while not self.__shutdown_event.is_set():
            try:
                segment_path = self.__upload_queue.get(block=True, timeout=5)
                self.__handle_segment(segment_path)
            except (TimeoutError, queue.Empty, KeyboardInterrupt):
                continue

        LOGGER.info("Uploader process is shutting down...")

    def __handle_segment(self, segment_path: str):
        LOGGER.info("Uploading %s", segment_path)
