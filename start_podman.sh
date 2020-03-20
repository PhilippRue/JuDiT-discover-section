#!/bin/bash -e


# debuging
set -x

# make sure previous run stopped
podman-compose -f docker-compose-podman.yml down 

# build container
podman-compose -f docker-compose-podman.yml build

# run container
podman-compose -f docker-compose-podman.yml up
