FROM msheiny/debian-jessie-systemd:latest

MAINTAINER Freedom of the Press
ENV GOPATH /tmp/logstash-filter-verifier

ENV GOLANG_VERSION 1.8
ENV GOLANG_DOWNLOAD_URL https://golang.org/dl/go$GOLANG_VERSION.linux-amd64.tar.gz
ENV GOLANG_DOWNLOAD_SHA256 53ab94104ee3923e228a2cb2116e5e462ad3ebaeea06ff04463479d7f12d27ca
ENV GOROOT /usr/local/go
ENV PATH $GOROOT/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-transport-https \
        binutils \
        git \
        make \
        curl \
        gnupg2 \
        ca-certificates \
        paxctl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL "$GOLANG_DOWNLOAD_URL" -o golang.tar.gz && \
    echo "$GOLANG_DOWNLOAD_SHA256  golang.tar.gz" | sha256sum -c - && \
    tar -C /usr/local -xzf golang.tar.gz && \
    rm golang.tar.gz && \
    mkdir $GOPATH && \
    cd $GOPATH && \
    go get -d github.com/magnusbaeck/logstash-filter-verifier && \
    cd src/github.com/magnusbaeck/logstash-filter-verifier && \
    make install && \
    cd /tmp && \
    rm -rf $GOPATH && \
    rm -rf $GOROOT

RUN apt-get update && apt-get install paxctld -y

RUN curl -fs https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
    echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" > /etc/apt/sources.list.d/elastic-5.x.list && \
    echo "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java m" >> /etc/paxctld.conf && \
    echo "/var/lib/dpkg/info/ca-certificates-java.postinst m" >> /etc/paxctld.conf && \
    echo "/etc/ca-certificates/update.d/jks-keystore m" >> /etc/paxctld.conf && \
    /etc/init.d/paxctld start && \
    mkdir -p /usr/share/man/man1/ && \
    apt-get update && \
    apt-get install -y openjdk-8-jre-headless 2> /dev/null && \
    apt-get install -y --allow-unauthenticated --no-install-recommends logstash && \
    /usr/share/logstash/bin/logstash-plugin install logstash-filter-de_dot && \
    rm -rf /var/lib/apt/lists/*

ADD scripts/start-up.sh /run/startup.sh
RUN chmod +x /run/startup.sh

ENTRYPOINT ["bash", "/run/startup.sh"]
CMD ["grsecurity.json", "all"]
