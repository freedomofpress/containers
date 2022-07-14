# sha256 as of 2022-07-07
FROM debian:bullseye-slim@sha256:f52f9aebdd310d504e0995601346735bb14da077c5d014e9f14017dadc915fe5
LABEL maintainer="Freedom of the Press Foundation"
LABEL description="Elastalert2 container based on Debian stable"
ENV TZ "America/Los_Angeles"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3-pip ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/jertel/elastalert2 /tmp/elastalert2-git
WORKDIR /tmp/elastalert2-git
RUN pip3 install -r requirements.txt
RUN python3 setup.py install

CMD ["elastalert"]
