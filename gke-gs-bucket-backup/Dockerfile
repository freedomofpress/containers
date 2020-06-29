# sha256 as of 2020-06-30 for 298.0.0-slim
FROM google/cloud-sdk@sha256:eaf964b5ac31bb7cc833c39c8c29a9002f9ec4c45311e9a66771cc5570a73723

COPY gs_bucket_sync.py /usr/local/bin

RUN adduser --disabled-password --uid 1000 gcloud_user
USER gcloud_user

ENTRYPOINT [ "/usr/local/bin/gs_bucket_sync.py" ]
