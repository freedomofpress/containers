# FPF Containers

A central place to keep track of all of our container images.

# Versioning

If a version is set in `version.txt` it is used as the image tag. These
should be an upstream version, then a YYYYMMDD date if applicable, then
our version (generally just a small integer), separated by `-`. Loosely
speaking, although Docker tags cannot use all the features of the `dpkg
--compare-versions` algorithm, if it DTRT you're good.
