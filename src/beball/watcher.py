import logging

from watchdog.observers import Observer

LOGGER = logging.getLogger(__name__)


class StreamSegmentWatcher:
    def __init__(self, src, handler):
        self.__src = src
        self.__handler = handler
        self.__observer = Observer()

    def start(self):
        LOGGER.debug("Watching for file events in %s", self.__src)
        self.__observer.schedule(self.__handler, self.__src, recursive=True)
        self.__observer.start()

    def stop(self):
        LOGGER.debug("Stopping file watcher in %s", self.__src)
        self.__observer.stop()
