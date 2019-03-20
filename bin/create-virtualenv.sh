#!/bin/bash
set -eu
cd "$(dirname "$0")"/..

if [[ -d env ]]
then
    echo "Virtualenv 'env' directory already exists, taking no action."
    exit 1
fi

python3 -m virtualenv env
env/bin/pip install -r requirements.txt
