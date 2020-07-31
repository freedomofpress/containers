# sha256 as of 2020-07-09 for logstash:6.7.2
FROM logstash@sha256:857d9a1f822101fe076e6e6a4a7df0426640424521e868393dac7e171baa9af5

LABEL MAINTAINER="Freedom of the Press"

ENV LS_VERIFIER_TAR https://github.com/magnusbaeck/logstash-filter-verifier/releases/download/1.5.0/logstash-filter-verifier_1.5.0_linux_amd64.tar.gz
ENV LS_VERIFIER_SHA256 9afbac697f87ec2e1773d2863e68bddd72b6d3f1d825334d62720dbc51a98b0e

USER root
RUN cd /tmp && \
    curl -sL $LS_VERIFIER_TAR -o ls-verifier.tar.gz && \
    echo "$LS_VERIFIER_SHA256  ls-verifier.tar.gz" | sha256sum -c - && \
    tar -C /usr/bin -xzf ls-verifier.tar.gz && \
    rm ls-verifier.tar.gz

ADD scripts/start-up.sh /run/startup.sh
RUN chmod +x /run/startup.sh
USER logstash

ENTRYPOINT ["bash", "/run/startup.sh"]
CMD ["grsecurity.json", "all"]
