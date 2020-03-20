#!/bin/bash -e


# debuging
set -x

# make sure previous run stopped
docker-compose -f docker-compose.yml down

# build container
docker-compose -f docker-compose.yml build

# run container
docker-compose -f docker-compose.yml up
