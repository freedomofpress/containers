# debian:buster-20191014
FROM debian@sha256:41f76363fd83982e14f7644486e1fb04812b3894aa4e396137c3435eaf05de88


ENV DOCKER_VER 19.03.4
ENV DOCKER_SHA256_x86_64 efef2ad32d262674501e712351be0df9dd31d6034b175d0020c8f5d5c9c3fd10


RUN apt-get update && \
    apt-get install -y flake8 make virtualenv ccontrol libpython3.7-dev \
            libffi-dev libssl-dev libyaml-dev python3-pip curl git &&\
    apt-get clean

RUN curl -L -o /tmp/docker-${DOCKER_VER}.tgz https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VER}.tgz; \
	echo "${DOCKER_SHA256_x86_64} /tmp/docker-${DOCKER_VER}.tgz" | sha256sum -c -; \
	cd /tmp && tar -xz -f /tmp/docker-${DOCKER_VER}.tgz; \
	mv /tmp/docker/* /usr/bin

CMD /bin/bash
