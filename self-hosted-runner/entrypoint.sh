#!/bin/bash

# Start docker daemon
service docker start

# Detect architecture
ARCH=$(uname -m)

if [ -n "$PERSONAL_ACCESS_TOKEN" ]; then
    echo "Using personal access token";
    runuser -u ubuntu -- ./config.sh \
        --unattended \
        --url $REPOSITORY_URL \
        --pat "$PERSONAL_ACCESS_TOKEN" \
        --name $RUNNER_NAME \
        --runnergroup $RUNNER_GROUP \
        --labels "${RUNNER_LABELS},${ARCH}" \
        --work /home/ubuntu/actions-runner \
        --replace;
else
    echo "Using registry token";
    runuser -u ubuntu -- ./config.sh \
        --unattended \
        --url $REPOSITORY_URL \
        --token "$REGISTRY_TOKEN" \
        --name $RUNNER_NAME \
        --runnergroup $RUNNER_GROUP \
        --labels "${RUNNER_LABELS},${ARCH}" \
        --work /home/ubuntu/actions-runner \
        --replace;
fi

exec runuser -u ubuntu -- ./run.sh
