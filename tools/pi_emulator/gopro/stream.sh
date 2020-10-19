#!/bin/bash
set -euo pipefail

TARGET_SERVER="${RTMP_SERVER:-localhost}"

echo "Waiting for RTMP server to become available.."

while ! nc -z "${TARGET_SERVER}" 80; do   
  sleep 1
done

STREAM_PATH="rtmp://${TARGET_SERVER}:1935/gopro/test"
echo "Streaming sample video in an infinite loop to ${STREAM_PATH}"

exec ffmpeg -re -stream_loop -1 -i "/usr/local/gopro/sample.mp4" -vcodec libx264 -f flv "${STREAM_PATH}"