FROM openjdk:8-jdk-slim-stretch

MAINTAINER Freedom of the Press

ENV LS_VERIFIER_TAR https://github.com/magnusbaeck/logstash-filter-verifier/releases/download/1.4.1/logstash-filter-verifier_1.4.1_linux_amd64.tar.gz
ENV LS_VERIFIER_SHA256 2c322c84d5a82532ee7aee56f06bb1046b62fe46a73e920be970301382decaf1
ARG LS_VER


RUN apt-get update && apt-get install -y --no-install-recommends \
        curl gnupg2 apt-transport-https && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/*

RUN curl -fs https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
    echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" > /etc/apt/sources.list.d/elastic.list && \
    apt-get update && apt-get install logstash=1:${LS_VER}-1 && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/apt/*

RUN cd /tmp && \
    curl -sL $LS_VERIFIER_TAR -o ls-verifier.tar.gz && \
    echo "$LS_VERIFIER_SHA256 ls-verifier.tar.gz" | sha256sum -c - && \
    tar -C /usr/bin -xzf ls-verifier.tar.gz

RUN chown logstash: -R /etc/logstash

ADD scripts/start-up.sh /run/startup.sh
RUN chmod +x /run/startup.sh
USER logstash

ENTRYPOINT ["bash", "/run/startup.sh"]
CMD ["grsecurity.json", "all"]
