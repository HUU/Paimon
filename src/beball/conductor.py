from watchdog.events import RegexMatchingEventHandler, FileSystemEvent


class Conductor(RegexMatchingEventHandler):
    SEGMENT_REGEX = [r".*\.ts$"]

    def __init__(self):
        super().__init__(self.SEGMENT_REGEX)

    def on_created(self, event: FileSystemEvent):
        print(event.src_path())

    def on_deleted(self, event: FileSystemEvent):
        print(event.src_path())

    def on_moved(self, event: FileSystemEvent):
        print(event.src_path())

    def on_modified(self, event: FileSystemEvent):
        print(event.src_path())
