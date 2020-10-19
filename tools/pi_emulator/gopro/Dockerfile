FROM debian:buster-slim

RUN apt-get update && \
    apt-get -y install ffmpeg netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY tools/pi_emulator/gopro/sample.mp4 tools/pi_emulator/gopro/stream.sh /usr/local/gopro/

CMD /usr/local/gopro/stream.sh