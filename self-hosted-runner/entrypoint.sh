#!/bin/bash

# Detect architecture
ARCH=$(uname -m)

RUN_AS_ROOT="${RUN_AS_ROOT:-true}"

# Start docker daemon
service docker start

if [ "$RUN_AS_ROOT" = "true" ]; then
    RUN_PREFIX=""
    export RUNNER_ALLOW_RUNASROOT=1
else
    RUN_PREFIX="runuser -u ubuntu --"
fi

if [ -n "$PERSONAL_ACCESS_TOKEN" ]; then
    echo "Using personal access token"
    $RUN_PREFIX ./config.sh \
        --unattended \
        --url $REPOSITORY_URL \
        --pat "$PERSONAL_ACCESS_TOKEN" \
        --name $RUNNER_NAME \
        --runnergroup $RUNNER_GROUP \
        --labels "${RUNNER_LABELS},${ARCH}" \
        --work /home/ubuntu/actions-runner \
        --replace
else
    echo "Using registry token"
    $RUN_PREFIX ./config.sh \
        --unattended \
        --url $REPOSITORY_URL \
        --token "$REGISTRY_TOKEN" \
        --name $RUNNER_NAME \
        --runnergroup $RUNNER_GROUP \
        --labels "${RUNNER_LABELS},${ARCH}" \
        --work /home/ubuntu/actions-runner \
        --replace
fi

exec $RUN_PREFIX ./run.sh
