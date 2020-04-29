#!/bin/bash

set -eux

COMMIT=$1
REMOTE="git@github.com:imrehg/faculty-github-actions.git"
DEPLOYMENT_KEY_PATH="/project/deployment_ssh_key"
# Private repo related setup
export GIT_SSH_COMMAND="/usr/bin/ssh -i ${DEPLOYMENT_KEY_PATH} -o StrictHostKeyChecking=no"

sudo rm -fr /code
sudo mkdir /code
sudo chown faculty:faculty /code

git clone "${REMOTE}" /code
cd /code
git checkout "$COMMIT"

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi
# Run the actual job
bash jobs/somejob.sh "${@:2}"
