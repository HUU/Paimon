FROM debian:buster-slim

RUN apt-get update && \
    apt-get -y install build-essential devscripts ffmpeg libpcre3 libpcre3-dev libssl-dev zlib1g-dev wget && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN wget https://github.com/arut/nginx-rtmp-module/archive/v1.2.1.tar.gz && \
    tar xvzf v1.2.1.tar.gz && \
    wget http://nginx.org/download/nginx-1.19.3.tar.gz && \
    tar xvzf nginx-1.19.3.tar.gz

RUN cd nginx-1.19.3 && \
    ./configure --prefix=/usr/local/nginx --with-http_ssl_module --add-module=../nginx-rtmp-module-1.2.1 --with-cc-opt=-Wno-error && \
    make -j 1 && \
    make install && \
    useradd -r nginx && \
    chown -R nginx:root /usr/local/nginx

COPY tools/pi_emulator/rtmp_server/nginx.conf /usr/local/nginx/conf/nginx.conf
COPY etc/beball/http.conf etc/beball/rtmp.conf /usr/local/nginx/conf/
COPY etc/beball/chunk_stream.sh /usr/local/beball/

VOLUME /tmp/hls

CMD ["/usr/local/nginx/sbin/nginx"]