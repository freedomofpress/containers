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

## Enacting a build

* Make sure you install the repo requirements via pipenv. Need to install pipenv?
  Follow [upstream documentation](ttps://pipenv.readthedocs.io/en/latest/install/#installing-pipenv).

* Either jump into a shell `pipenv shell` or you can run the following command
  with `pipenv run _____`

* Run `./build.py $<name_of_local_container_dir>` .. I like to take advantage of
  the tab completion in terminal here when selecting a container to build.
