# sha256 as of 2020-10-06 for buster-slim
FROM debian@sha256:8d81110c3f93a777e3f4053a6b18b70e4a1003655b8c2664bdf18b19043f99d9
LABEL maintainer="Freedom of the Press Foundation"
LABEL description="Elastalert container based on Debian stable"
ENV TZ "America/Los_Angeles"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3 python3-pip ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fixes SSL verification problem with Slack notifications, see
# https://github.com/Yelp/elastalert/issues/2955
# https://github.com/Yelp/elastalert/pull/2760
# https://github.com/JeffAshton/elastalert/commit/340ce3626b80be791416b7af7176ec110d2a3815
RUN git clone https://github.com/JeffAshton/elastalert.git /tmp/elastalert-git
WORKDIR /tmp/elastalert-git
# RUN git checkout fixing-slack-ssl-verification
RUN git checkout 340ce3626b80be791416b7af7176ec110d2a3815
RUN python3 setup.py install

# A few tweaks for compatibility. The "elastalert" PyPI config is unduly
# liberal in its dependency pinning.
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

CMD ["elastalert"]
