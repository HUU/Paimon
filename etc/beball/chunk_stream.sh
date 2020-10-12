#!/bin/bash
set -euo pipefail

app=${1}
name=${2}

echo "Starting to chunk stream ${app}/${name}..."

mkdir -p "/tmp/hls/${name}"
exec ffmpeg -re -i rtmp://localhost:1935/${app}/${name} -codec copy -flags +cgop -g 30 -hls_time 5 /tmp/hls/${name}/stream.m3u8