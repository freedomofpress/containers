FROM fedora:25
LABEL maintainer="Freedom of the Press Foundation"
LABEL description="RedHat tooling for building RPMs"
ARG FEDORA_PKGR_VER


RUN echo "${FEDORA_PKGR_VER}"

RUN dnf update -y && \
    dnf install -y \
    fedora-packager-${FEDORA_PKGR_VER}.noarch \
    make \
    python3-cryptography \
    python3-devel \
    python3-requests \
    python3-setuptools \
    vim && \
    yum clean all

ENV HOME /home/user
RUN useradd --create-home --home-dir $HOME user \
    && chown -R user:user $HOME && \
    su -c rpmdev-setuptree user

WORKDIR $HOME/rpmbuild
VOLUME $HOME/rpmbuild

USER user

CMD ["/usr/bin/bash"]
