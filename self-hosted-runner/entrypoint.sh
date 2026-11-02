#!/bin/bash

# Detect architecture
ARCH=$(uname -m)

RUN_AS_ROOT="${RUN_AS_ROOT:-true}"

# Start docker daemon. A restarted container keeps the previous run's
# /var/run/docker.pid, and dockerd refuses to start while that PID belongs to
# another process of the new run. Nothing can be using it before this point.
rm -f /var/run/docker.pid
service docker start
# Exit instead of registering a runner that fails every container job.
if ! timeout 60 bash -c 'until docker info >/dev/null 2>&1; do sleep 1; done'; then
    echo "Docker daemon did not start:" >&2
    tail -n 20 /var/log/docker.log >&2
    exit 1
fi

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
