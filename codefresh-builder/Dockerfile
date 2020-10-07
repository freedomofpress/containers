# sha256 as of 2020-10-06 for buster-slim
FROM debian@sha256:8d81110c3f93a777e3f4053a6b18b70e4a1003655b8c2664bdf18b19043f99d9

RUN apt-get update && \
    apt-get install -y make curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY codefresh-prepare /usr/local/bin
