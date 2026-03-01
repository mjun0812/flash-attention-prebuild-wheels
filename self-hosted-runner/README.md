# Self-Hosted Runner Setup

This directory contains the Docker-based self-hosted runner configuration for building flash-attention wheels.

In some version combinations, you cannot build wheels on GitHub-hosted runners due to job time limitations.
To build the wheels for these versions, you can use self-hosted runners.

## Prerequisites

- Docker and Docker Compose
- GitHub Personal Access Token or Runner Registration Token

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

### 2. Create environment file

Create an environment file from the template.

```bash
cp env.template .env
```

### 3. Edit the environment file

Set the required variables in the `.env` file.

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
```

### 5. Build and run

```bash
docker compose build runner
docker compose up -d runner
```

## Configuration

### Environment Variables

| Variable               | Required | Description                                   |
| ---------------------- | -------- | --------------------------------------------- |
| `PERSONAL_ACCESS_TOKEN`| Either   | GitHub Personal Access Token                   |
| `REGISTRY_TOKEN`       | Either   | One-time Runner Registration Token             |
| `RUNNER_LABELS`        | No       | Comma-separated labels (default: `Linux,self-hosted`) |

### compose.yml Variables

| Variable         | Description                                    | Default                  |
| ---------------- | ---------------------------------------------- | ------------------------ |
| `REPOSITORY_URL` | Target GitHub repository URL                   | This repository          |
| `RUNNER_NAME`    | Name of the runner                             | `self-hosted-runner`     |
| `RUNNER_GROUP`   | Runner group                                   | `default`                |

### Dockerfile Build Args

| Arg                 | Description                        | Default    |
| ------------------- | ---------------------------------- | ---------- |
| `GH_RUNNER_VERSION` | GitHub Actions Runner version      | `2.331.0`  |

## Architecture

The container runs the following:

1. Starts Docker daemon (Docker-in-Docker via privileged mode)
2. Configures the GitHub Actions runner with the provided credentials
3. Starts the runner process

The container uses `ubuntu:24.04` as base image and includes Docker CE for building wheels inside the runner.
