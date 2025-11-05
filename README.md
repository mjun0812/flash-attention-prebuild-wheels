# flash-attention pre-build wheels

This repository provides wheels for the pre-built [flash-attention](https://github.com/Dao-AILab/flash-attention).

Since building flash-attention takes a **very long time** and is resource-intensive,
I also build and provide combinations of CUDA and PyTorch that are not officially distributed.

The building Github Actions Workflow can be found [here](./.github/workflows/build.yml).  
The built packages are available on the [release page](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases).

**This repository uses a self-hosted runner and AWS CodeBuild for building the wheels. If you find this project helpful, please consider sponsoring to help maintain the infrastructure!**

[![github-sponsor](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#white)](https://github.com/sponsors/mjun0812)

[![buy-me-a-coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/mjun0812)

## Table of Contents

- [flash-attention pre-build wheels](#flash-attention-pre-build-wheels)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Packages](#packages)
  - [History](#history)
  - [Self build](#self-build)
    - [Self-Hosted Runner Build](#self-hosted-runner-build)
  - [Original Repository](#original-repository)

## Install

1. Select the versions for Python, CUDA, PyTorch, and flash_attn.

```bash
flash_attn-[flash_attn Version]+cu[CUDA Version]torch[PyTorch Version]-cp[Python Version]-cp[Python Version]-linux_x86_64.whl

# Example: Python 3.11, CUDA 12.4, PyTorch 2.5, and flash_attn 2.6.3
flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl
```

2. Find the corresponding version of a wheel from the [Packages](./docs/packages.md) page and [releases](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases) page.

3. Direct Install or Download and Local Install

```bash
# Direct Install
pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.0.0/flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl

# Download and Local Install
wget https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.0.0/flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl
pip install ./flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl
```

## Packages

See [./docs/packages.md](./docs/packages.md) for the full list of available packages.

## History

History of this repository is available [here](./docs/release_history.md).

## Self build

If you cannot find the version you are looking for, you can fork this repository and create a wheel on GitHub Actions.

1. Fork this repository
2. Edit workflow file [`.github/workflows/build.yml`](https://github.com/mjun0812/flash-attention-prebuild-wheels/blob/main/.github/workflows/build.yml) to set the version you want to build.
3. Add tag `v*.*.*` to trigger the build workflow.

Please note that depending on the combination of versions, it may not be possible to build.

### Self-Hosted Runner Build

In some version combinations, you cannot build wheels on GitHub-hosted runners due to job time limitations.
To build the wheels for these versions, you can use self-hosted runners.

```bash
git clone https://github.com/mjun0812/flash-attention-prebuild-wheels.git
cd self-hosted-runner
cp env.template env
```

Edit `env` file to set the environment variables.

```bash
# Edit env
PERSONAL_ACCESS_TOKEN=[Github Personal Access Token]
```

Edit compose.yml file if you use repository folked from this repository.

```yaml
services:
  runner:
    privileged: true
    build:
      context: .
      dockerfile: Dockerfile
      args:
        REPOSITORY_URL: [Target Repository URL]
        PERSONAL_ACCESS_TOKEN: $PERSONAL_ACCESS_TOKEN
        GH_RUNNER_VERSION: 2.324.0
        RUNNER_NAME: self-hosted-runner
        RUNNER_GROUP: default
        RUNNER_LABELS: self-hosted
        TARGET_ARCH: x64
```

Then, build and run the docker container.

```bash
# Build and run
docker compose build
docker compose up -d
```

## Original Repository

[repo](https://github.com/Dao-AILab/flash-attention)

```bibtex
@inproceedings{dao2022flashattention,
  title={Flash{A}ttention: Fast and Memory-Efficient Exact Attention with {IO}-Awareness},
  author={Dao, Tri and Fu, Daniel Y. and Ermon, Stefano and Rudra, Atri and R{\'e}, Christopher},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  year={2022}
}
@inproceedings{dao2023flashattention2,
  title={Flash{A}ttention-2: Faster Attention with Better Parallelism and Work Partitioning},
  author={Dao, Tri},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2024}
}
```
