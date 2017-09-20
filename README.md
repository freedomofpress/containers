# FPF Containers

A central place to keep track of all of our container images.

## Meta files
To help us keep track of the metadata regarding each image
lets store that info in a `meta.yml` file in each directory.

Right now I just have 

* `repo` - the destination of where the image is hosted
* `tag` - the current tag of the adjacent dockerfile in the folder

For example in `circleci-docker/meta.yml`:

```yaml
---
repo: "quay.io/freedomofpress/circleci-docker"
tag: "v2"
```
