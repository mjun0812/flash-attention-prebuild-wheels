# Self-Hosted Runner Setup

This directory contains the Docker-based self-hosted runner configuration for building flash-attention wheels.

In some version combinations, you cannot build wheels on GitHub-hosted runners due to job time limitations.
To build the wheels for these versions, you can use self-hosted runners.

## Services

| Service      | Description                                             | Architecture |
| ------------ | ------------------------------------------------------- | ------------ |
| `runner`     | Native architecture runner with Docker-in-Docker (DinD) | Host native  |
| `runner-arm` | ARM64 runner via QEMU emulation (no DinD)               | arm64        |

The `runner` service uses Docker-in-Docker to run container-based workflow jobs.
The `runner-arm` service runs under QEMU emulation and is intended for no-container workflow jobs that execute directly on the runner.

## Prerequisites

- Docker and Docker Compose
- QEMU user static binaries (for `runner-arm`)
- GitHub Personal Access Token or Runner Registration Token

To set up QEMU for ARM64 emulation:

```bash
sudo apt install qemu-user-static
```

## Getting One-Time Registry Token for GitHub Actions Runner

```bash
gh api \
  -X POST \
  /repos/[OWNER]/[REPOSITORY]/actions/runners/registration-token
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mjun0812/flash-attention-prebuild-wheels.git
cd flash-attention-prebuild-wheels/self-hosted-runner
```

### 2. Create environment files

Create environment files from the template.

```bash
# For native runner
cp env.template .env
# For ARM64 QEMU runner
cp env.template .env.arm
```

### 3. Edit the environment files

Set the required variables in each `.env` file.

```bash
# GitHub Personal Access Token (recommended)
PERSONAL_ACCESS_TOKEN=[Github Personal Access Token]
# or One-time Registry Token for GitHub Actions Runner
REGISTRY_TOKEN=[Runner Registry Token]

# Optional: Custom labels for the runner
RUNNER_LABELS=Linux,self-hosted
```

> **Note:** You must set either `PERSONAL_ACCESS_TOKEN` or `REGISTRY_TOKEN`. If both are set, `PERSONAL_ACCESS_TOKEN` takes precedence.

### 4. Edit compose.yml (for forked repositories)

If you use a repository forked from this repository, edit the `REPOSITORY_URL` in `compose.yml`.

```yaml
services:
  runner:
    environment:
      REPOSITORY_URL: https://github.com/[YOUR_USERNAME]/flash-attention-prebuild-wheels
  runner-arm:
    environment:
      REPOSITORY_URL: https://github.com/[YOUR_USERNAME]/flash-attention-prebuild-wheels
```

### 5. Build and run

```bash
# Native runner
docker compose build runner
docker compose up -d runner

# ARM64 QEMU runner
docker compose build runner-arm
docker compose up -d runner-arm
```

## Configuration

### Environment Variables

| Variable                | Required | Description                                           |
| ----------------------- | -------- | ----------------------------------------------------- |
| `PERSONAL_ACCESS_TOKEN` | Either   | GitHub Personal Access Token                          |
| `REGISTRY_TOKEN`        | Either   | One-time Runner Registration Token                    |
| `RUNNER_LABELS`         | No       | Comma-separated labels (default: `Linux,self-hosted`) |

### compose.yml Variables

| Variable         | Description                  | Default (`runner`)   | Default (`runner-arm`)        |
| ---------------- | ---------------------------- | -------------------- | ----------------------------- |
| `REPOSITORY_URL` | Target GitHub repository URL | This repository      | This repository               |
| `RUNNER_NAME`    | Name of the runner           | `self-hosted-runner` | `self-hosted-runner-arm-qemu` |
| `RUNNER_GROUP`   | Runner group                 | `default`            | `default`                     |

### Dockerfile Build Args

| Arg                 | Description                   | Default   |
| ------------------- | ----------------------------- | --------- |
| `GH_RUNNER_VERSION` | GitHub Actions Runner version | `2.331.0` |

## Architecture

### Native runner (`runner`)

1. Starts Docker daemon (Docker-in-Docker via privileged mode)
2. Configures the GitHub Actions runner with the provided credentials
3. Starts the runner process

### ARM64 QEMU runner (`runner-arm`)

1. Detects aarch64 architecture and applies QEMU workarounds (disables iptables/ip6tables)
2. Starts Docker daemon
3. Configures the GitHub Actions runner with the provided credentials
4. Starts the runner process

Both containers use `ubuntu:24.04` as the base image. The native runner includes Docker CE for running container-based workflow jobs.
