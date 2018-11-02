#!/usr/bin/env python3
"""
Builds docker images using specs from folders and metadata config files.
"""

import argparse
import os
import shlex
import subprocess
import yaml


CUR_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def get_container_names(dir_name=CUR_DIRECTORY):
    """
        Get me a list of sub-directories that contain a meta.yml.
        Assume these are container names we are interested in
    """
    containers = []

    for dir in os.listdir(dir_name):
        try:
            if ('meta.yml' in os.listdir(dir) and
                    'Dockerfile' in os.listdir(dir)):
                containers.append(dir)
        except NotADirectoryError:
            continue

    return containers


def extract_metadata(rootdir):
    """ Provide root directory of container files, reads that folders meta.yml, and returns the yaml object """
    with open(os.path.join(rootdir, 'meta.yml'), 'r') as f:
        return yaml.load(f.read())


def run_command(command):
    """
    Takes in a string command, runs said command as a subprocess, print to stdout live

    Taken from https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
    """
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


def build(image_name, dir=CUR_DIRECTORY):
    """
        Build docker image.

        Assumes there is a dir structure of ./<container_name_dir>/
        With at least `meta.yml` and `Dockerfile` within that folder.
    """
    container_dir = os.path.join(dir, image_name)

    meta_data = extract_metadata(container_dir)

    # If build args exist in metadata. lets pull em out!
    try:
        opt_args = ""
        for build_arg in meta_data['args']:
            opt_args += "--build-arg={}={} ".format(
                        build_arg,
                        meta_data['args'][build_arg])
    except KeyError:
        pass

    # Build docker command
    docker_cmd = ("docker build {opt} -t {tag}"
                  " -f {dockerfile} {context}").format(
                        opt=opt_args,
                        tag=':'.join([meta_data['repo'], meta_data['tag']]),
                        dockerfile=os.path.join(container_dir, 'Dockerfile'),
                        context=container_dir)

    print("Running '{}'".format(docker_cmd))
    run_command(docker_cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    # Basically a folder that has a meta.yml and a Dockerfile
    parser.add_argument('container',
                        type=str,
                        help='container to build',
                        choices=get_container_names())

    args = parser.parse_args()

    build(args.container)
