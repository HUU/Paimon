#!/bin/bash
set -euo pipefail

docker-compose -f tools/pi_emulator/docker-compose.yml down
sudo rm -rf /tmp/hls/*