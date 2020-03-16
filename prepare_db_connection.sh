#!/bin/bash -e

# This script is executed whenever the docker container is (re)started.

#===============================================================================
# debuging
set -x

#===============================================================================

# write AiiDA config file
echo "writing config file: $AIIDA_PATH/config.json"
mkdir -p $AIIDA_PATH
cat > $AIIDA_PATH/config.json <<EOF
{
    "CONFIG_VERSION": {
        "CURRENT": 3,
        "OLDEST_COMPATIBLE": 3
    },
    "default_profile": "judit",
    "profiles": {
        "${AIIDA_PROFILE}": {
            "AIIDADB_ENGINE": "${AIIDADB_ENGINE}",
            "AIIDADB_PASS": "${AIIDADB_PASS}",
            "AIIDADB_NAME": "${AIIDADB_NAME}",
            "AIIDADB_HOST": "${AIIDADB_HOST}",
            "AIIDADB_BACKEND": "${AIIDADB_BACKEND}",
            "AIIDADB_PORT": "${AIIDADB_PORT}",
            "PROFILE_UUID": "d1ebf3111f8944dfb6ee445aa7bccebc",
            "default_user_email": "${default_user_email}",
            "AIIDADB_REPOSITORY_URI": "${AIIDADB_REPOSITORY_URI}",
            "AIIDADB_USER": "${AIIDADB_USER}",
            "options": {}
        }
    }
}
EOF

echo "contents of config file:"
cat $AIIDA_PATH/config.json

#EOF
