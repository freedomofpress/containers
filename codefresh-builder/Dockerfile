# sha256 as of 2020-07-30 for buster-slim
FROM debian@sha256:79326248a982be0b36e8280f906916fceffdd5c17a298b14446e5e72cc822fe7

RUN apt-get update && \
    apt-get install -y make curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
