FROM ubuntu:24.04

ARG REPOSITORY_URL="https://github.com/user/repo"
ARG GH_RUNNER_VERSION="2.329.0"
ARG RUNNER_NAME="self-hosted-github-actions-runner"
ARG RUNNER_GROUP="default"
ARG RUNNER_LABELS="self-hosted,Linux"
ARG TARGET_ARCH="x64"
ARG PERSONAL_ACCESS_TOKEN=""
ARG REGISTRY_TOKEN=""

ENV DEBIAN_FRONTEND=noninteractive \
    AGENT_TOOLSDIRECTORY=/opt/hostedtoolcache

RUN mkdir -p /opt/hostedtoolcache \
    && chown -R ubuntu:ubuntu /opt/hostedtoolcache

RUN apt-get update && apt-get install -y --no-install-recommends\
    curl \
    ca-certificates \
    sudo \
    software-properties-common \
    wget \
    unzip \
    zip \
    git \
    libc-bin \
    && rm -rf /var/lib/apt/lists/*

# Install Docker
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    # Add the repository to Apt sources:
    && echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    docker-ce-cli \
    docker-ce \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# Install dotnet
RUN add-apt-repository ppa:dotnet/backports

# ubuntu >= 24.04 image has user named 'ubuntu'
RUN usermod -aG sudo ubuntu \
    && usermod -aG docker ubuntu

# Allow sudo without password
RUN echo '%sudo ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

USER ubuntu
WORKDIR /home/ubuntu

RUN curl -fsSL -o actions-runner.tar.gz -L "https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-${TARGET_ARCH}-${GH_RUNNER_VERSION}.tar.gz" \
    && tar xf actions-runner.tar.gz \
    && rm actions-runner.tar.gz \
    && sudo ./bin/installdependencies.sh \
    && if [ -n "$PERSONAL_ACCESS_TOKEN" ]; then \
    ./config.sh \
    --unattended \
    --url $REPOSITORY_URL \
    --pat "$PERSONAL_ACCESS_TOKEN" \
    --name $RUNNER_NAME \
    --runnergroup $RUNNER_GROUP \
    --labels "${RUNNER_LABELS},${TARGET_ARCH}" \
    --work /home/ubuntu/actions-runner \
    --replace; \
    else \
    ./config.sh \
    --unattended \
    --url $REPOSITORY_URL \
    --token "$REGISTRY_TOKEN" \
    --name $RUNNER_NAME \
    --runnergroup $RUNNER_GROUP \
    --labels "${RUNNER_LABELS},${TARGET_ARCH}" \
    --work /home/ubuntu/actions-runner \
    --replace; \
    fi

CMD ["./run.sh"]
