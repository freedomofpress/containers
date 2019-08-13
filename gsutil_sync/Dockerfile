ARG GCLOUD_HASH
FROM google/cloud-sdk@sha256:${GCLOUD_HASH}

# Create a new dedicated gcloud tooling user
RUN adduser gcloud_user -g "" -D
ENV PATH /google-cloud-sdk/bin:$PATH
