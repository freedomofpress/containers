FROM ubuntu@sha256:132f5164abac16b04d918547e4d0327bbd98a42ab33ef21d017d962cec2cb5aa

LABEL maintainer="Freedom of the Press Foundation"

COPY config/00redirects /etc/apt/apt.conf.d/00redirects
RUN apt-get update &&\
    apt-get install --no-install-recommends -y\
        git gcc g++ python3 python3-dev virtualenv \
        libxml2-dev libxslt-dev zlib1g-dev libjpeg-dev \
        libpq-dev libffi-dev locales locales-all \
        python sudo bash ca-certificates paxctl &&\
    apt-get clean && rm -rf /var/lib/apt/lists/* &&\
    rm -rf /usr/share/doc/ && rm -rf /usr/share/man &&\
    rm -rf /usr/share/locale

# http://bugs.python.org/issue19846
# At the moment, setting "LANG=C" on a Linux system *fundamentally breaks py3
ENV LANG C.UTF-8
