#!/bin/bash

# Start docker daemon
sudo service docker start

if [ -n "$PERSONAL_ACCESS_TOKEN" ]; then
    echo "Using personal access token";
    ./config.sh \
        --unattended \
        --url $REPOSITORY_URL \
        --pat "$PERSONAL_ACCESS_TOKEN" \
        --name $RUNNER_NAME \
        --runnergroup $RUNNER_GROUP \
        --labels "${RUNNER_LABELS},${TARGET_ARCH}" \
        --work /home/ubuntu/actions-runner \
        --replace;
else
    echo "Using registry token";
    ./config.sh \
        --unattended \
        --url $REPOSITORY_URL \
        --token "$REGISTRY_TOKEN" \
        --name $RUNNER_NAME \
        --runnergroup $RUNNER_GROUP \
        --labels "${RUNNER_LABELS},${TARGET_ARCH}" \
        --work /home/ubuntu/actions-runner \
        --replace;
fi

exec "./run.sh"
