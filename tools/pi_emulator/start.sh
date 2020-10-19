#!/bin/bash
set -euo pipefail

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$SCRIPTPATH/../.." # root of the project

mkdir -p /tmp/hls
sudo rm -rf /tmp/hls/*

docker-compose -f tools/pi_emulator/docker-compose.yml up -d


