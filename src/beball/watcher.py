from watchdog.observers import Observer


class StreamSegmentWatcher:
    def __init__(self, src, handler):
        self.__src = src
        self.__handler = handler
        self.__observer = Observer()

    def start(self):
        self.__observer.schedule(self.__handler, self.__src, recursive=True)
        self.__observer.start()

    def stop(self):
        self.__observer.stop()
