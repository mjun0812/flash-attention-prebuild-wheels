#!/bin/bash

ARCH=$(uname -m)

if [ "$ARCH" = "aarch64" ]; then
    echo "Architecture is aarch64 (ARM64). Applying QEMU workarounds..."
    mkdir -p /etc/docker
    cat <<EOF > /etc/docker/daemon.json
{
  "iptables": false,
  "ip6tables": false
}
EOF
fi

# Start docker daemon
service docker start

if [ -n "$PERSONAL_ACCESS_TOKEN" ]; then
    echo "Using personal access token";
    runuser -u ubuntu -- ./config.sh \
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
    runuser -u ubuntu -- ./config.sh \
        --unattended \
        --url $REPOSITORY_URL \
        --token "$REGISTRY_TOKEN" \
        --name $RUNNER_NAME \
        --runnergroup $RUNNER_GROUP \
        --labels "${RUNNER_LABELS},${TARGET_ARCH}" \
        --work /home/ubuntu/actions-runner \
        --replace;
fi

exec runuser -u ubuntu -- ./run.sh
