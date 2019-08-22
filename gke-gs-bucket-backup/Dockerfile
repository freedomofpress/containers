# tag 258.0.0
ARG CLOUD_SDK_HASH='d026fcb44de9f3ac58ed959afa892d8216de858dc69b370e001d641a4e362437'

FROM google/cloud-sdk@sha256:${CLOUD_SDK_HASH}

COPY gs_bucket_sync.py /usr/local/bin

RUN adduser --disabled-password --gecos "" gcloud_user
USER gcloud_user
ENV PATH "$PATH:/opt/google-cloud-sdk/bin/"


ENTRYPOINT [ "/usr/local/bin/gs_bucket_sync.py" ]
