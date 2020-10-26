import m3u8
import logging

from pathlib import PurePath
from watchdog.events import RegexMatchingEventHandler, FileSystemEvent
from multiprocessing import Queue
from typing import Dict

LOGGER = logging.getLogger(__name__)


class Conductor(RegexMatchingEventHandler):
    SEGMENT_REGEX = [r".*\.(ts|m3u8)$"]

    def __init__(self, upload_queue: Queue):
        super().__init__(self.SEGMENT_REGEX)
        self.__in_progress_segments: Dict[str, str] = dict()
        self.__upload_queue: Queue = upload_queue

    def on_created(self, event: FileSystemEvent):
        if event.src_path.endswith(".ts"):
            self.__in_progress_segments[PurePath(event.src_path).name] = event.src_path
        elif event.src_path.endswith(".m3u8"):
            self.__handle_m3u8(event.src_path)

    def on_modified(self, event: FileSystemEvent):
        if event.src_path.endswith(".m3u8"):
            self.__handle_m3u8(event.src_path)

    def __handle_m3u8(self, m3u8_path: str):
        playlist = m3u8.load(m3u8_path)
        LOGGER.debug(
            "Playlist contains these segments: %s",
            list(map(lambda s: s.uri, playlist.segments)),
        )
        for segment in playlist.segments:
            if segment.uri in self.__in_progress_segments:
                LOGGER.info(
                    "Segment %s (%ss) is ready, enqueuing.",
                    segment.uri,
                    segment.duration,
                )
                stream_path = self.__in_progress_segments.pop(segment.uri)
                self.__upload_queue.put(stream_path)
        LOGGER.debug("Still tracking these segments: %s", self.__in_progress_segments)
