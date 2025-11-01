# flash-attention pre-build wheels

This repository provides wheels for the pre-built [flash-attention](https://github.com/Dao-AILab/flash-attention).

Since building flash-attention takes a **very long time** and is resource-intensive,
I also build and provide combinations of CUDA and PyTorch that are not officially distributed.

The building Github Actions Workflow can be found [here](./.github/workflows/build.yml).  
The built packages are available on the [release page](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases).

**This repository uses a self-hosted runner and AWS CodeBuild for building the wheels. If you find this project helpful, please consider sponsoring to help maintain the infrastructure!**

[![fund](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/mjun0812)

## Table of Contents

- [Install](#install)
- [Packages](#packages)
  - [Linux x86_64](#linux-x86_64)
  - [Windows x86_64](#windows-x86_64)
- [Self-build runner](#self-build)
- [History](#history)
- [Original Repository](#original-repository)

## Install

1. Select the versions for Python, CUDA, PyTorch, and flash_attn.

```bash
flash_attn-[flash_attn Version]+cu[CUDA Version]torch[PyTorch Version]-cp[Python Version]-cp[Python Version]-linux_x86_64.whl

# Example: Python 3.11, CUDA 12.4, PyTorch 2.5, and flash_attn 2.6.3
flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl
```

2. Find the corresponding version of a wheel from the below [Package section](#packages) and [releases](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases)

3. Direct Install or Download and Local Install

```bash
# Direct Install
pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.0.0/flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl

# Download and Local Install
wget https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.0.0/flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl
pip install ./flash_attn-2.6.3+cu124torch2.5-cp312-cp312-linux_x86_64.whl
```

## Packages

### Linux x86_64

#### Flash-Attention 2.8.3

<details>
<summary>Packages for Flash-Attention 2.8.3</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.13 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.13 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.13 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.13 | 2.8 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.8 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.7 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.7 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.6 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.6 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.6 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.12 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.12 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.12 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.12 | 2.8 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.8 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.7 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.7 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.6 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.6 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.6 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.5 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.5 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.5 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.12 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.11 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.11 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.11 | 2.8 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.8 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.7 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.7 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.6 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.6 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.6 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.5 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.5 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.5 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.11 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.10 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.10 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.10 | 2.8 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.8 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.7 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.7 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.6 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.6 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.6 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.5 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.5 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.5 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.10 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11) |
| 3.9 | 2.8 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.7 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.6 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.5 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |

</details>

#### Flash-Attention 2.8.2

<details>
<summary>Packages for Flash-Attention 2.8.2</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.8.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.8.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.8.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.7.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.6.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.5.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.8.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.8.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.8.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.7.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.6.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.5.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.8.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.8.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.8.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.7.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.6.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.5.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |

</details>

#### Flash-Attention 2.8.1

<details>
<summary>Packages for Flash-Attention 2.8.1</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.12 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.12 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.12 | 2.4.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.11 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.11 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.11 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.11 | 2.4.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.10 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.10 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.10 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |
| 3.10 | 2.4.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13) |

</details>

#### Flash-Attention 2.8.0

<details>
<summary>Packages for Flash-Attention 2.8.0</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.12 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.12 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.12 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.12 | 2.4.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.4.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.4.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12) |

</details>

#### Flash-Attention 2.7.4

<details>
<summary>Packages for Flash-Attention 2.7.4</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.8 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1) |
| 3.12 | 2.7 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.10) |
| 3.12 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0) |
| 3.12 | 2.6 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.6 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.5 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.5 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.12 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.8 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1) |
| 3.11 | 2.7 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.10) |
| 3.11 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0) |
| 3.11 | 2.6 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.6 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.5 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.5 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.11 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.8 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1) |
| 3.10 | 2.7 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.10) |
| 3.10 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0) |
| 3.10 | 2.6 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.6 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.5 | 12.9 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.5 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |
| 3.10 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18) |

</details>

#### Flash-Attention 2.7.4.post1

<details>
<summary>Packages for Flash-Attention 2.7.4.post1</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.12 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.1.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.0.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.1.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.0.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.10 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.1.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.0.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |

</details>

#### Flash-Attention 2.7.3

<details>
<summary>Packages for Flash-Attention 2.7.3</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.12 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.11 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |
| 3.10 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4) |

</details>

#### Flash-Attention 2.7.2.post1

<details>
<summary>Packages for Flash-Attention 2.7.2.post1</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.12 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.11 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |
| 3.10 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3) |

</details>

#### Flash-Attention 2.7.0.post2

<details>
<summary>Packages for Flash-Attention 2.7.0.post2</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |

</details>

#### Flash-Attention 2.6.3

<details>
<summary>Packages for Flash-Attention 2.6.3</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.13 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.13 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.13 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.12 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.12 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.12 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.12 | 2.8.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.8.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.8.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.12 | 2.7.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.12 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.6.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.5.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.12 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release5](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.12 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.11 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.11 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.11 | 2.8.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.8.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.8.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.11 | 2.7.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.11 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.6.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.5.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.11 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release5](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.11 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.9 | 13.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18) |
| 3.10 | 2.9 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.10 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17) |
| 3.10 | 2.8.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.8.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.8.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.10 | 2.7.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.7.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.10 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.6.0 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.6.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.5.1 | 12.9.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.5.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14) |
| 3.10 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release5](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release4](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5) |
| 3.10 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.9 | 2.8 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.7 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.6 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.5 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |
| 3.9 | 2.5 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16) |

</details>

#### Flash-Attention 2.5.9

<details>
<summary>Packages for Flash-Attention 2.5.9</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.12 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.12 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.11 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.11 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.10 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.10 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |

</details>

#### Flash-Attention 2.5.6

<details>
<summary>Packages for Flash-Attention 2.5.6</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |

</details>

#### Flash-Attention 2.4.3

<details>
<summary>Packages for Flash-Attention 2.4.3</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.12 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.12 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.12 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.12 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.12 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.11 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.11 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.11 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.11 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.11 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.8.0.dev20250523 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0) |
| 3.10 | 2.7.1 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.7.0 | 12.8.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9) |
| 3.10 | 2.7.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.7.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.6.0 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8) |
| 3.10 | 2.5.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.5.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release3](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.4.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.3.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.3.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6) |
| 3.10 | 2.2.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.2.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.1.2 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 12.1.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |
| 3.10 | 2.0.1 | 11.8.0 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2) |

</details>

### Windows x86_64

#### Flash-Attention 2.8.3

<details>
<summary>Packages for Flash-Attention 2.8.3</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.13 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.12 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |
| 3.11 | 2.9 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15) |

</details>

#### Flash-Attention 2.8.2

<details>
<summary>Packages for Flash-Attention 2.8.2</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.13 | 2.8 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.8 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.7 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.7 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.6 | 12.6 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.13 | 2.6 | 12.4 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12) |
| 3.12 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.12 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.11 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.11 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.10 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.10 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |

</details>

#### Flash-Attention 2.7.4

<details>
<summary>Packages for Flash-Attention 2.7.4</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.12 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.11 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10), [Release2](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.9) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.8 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.10 | 2.7 | 12.8 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |

</details>

#### Flash-Attention 2.6.3

<details>
<summary>Packages for Flash-Attention 2.6.3</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.6.0 | 12.6.3 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.1) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |

</details>

#### Flash-Attention 2.5.9

<details>
<summary>Packages for Flash-Attention 2.5.9</summary>

| Python | PyTorch | CUDA | package |
| ------ | ------- | ---- | ------- |
| 3.12 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.12 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.11 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.6.0 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.5.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |
| 3.10 | 2.4.1 | 12.4.1 | [Release1](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9) |

</details>


## History

### v0.4.18

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.18)

#### Linux x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.6.3, 2.8.3 | 3.10, 3.11, 3.12, 3.13 | 2.9 | 13.0 |

### v0.4.17

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.17)

#### Linux x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.6.3, 2.8.3 | 3.10, 3.11, 3.12, 3.13 | 2.9 | 12.6, 12.8 |

### v0.4.16

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.16)

#### Linux x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.6.3, 2.8.3 | 3.9 | 2.5, 2.6, 2.7, 2.8 | 12.4, 12.6 |

### v0.4.15

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.15)

#### Linux x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.8.3 | 3.11, 3.12, 3.13 | 2.9 | 12.6, 12.8 |

#### Windows x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.8.3 | 3.11, 3.12, 3.13 | 2.9 | 12.6 |

### v0.4.12

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.12)

#### Linux x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.8.3 | 3.13 | 2.6, 2.7, 2.8 | 12.4, 12.6, 12.8, 12.9 |

#### Windows x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.8.2 | 3.13 | 2.6, 2.7, 2.8 | 12.4, 12.6 |

### v0.4.11

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.11)

#### Linux x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.8.3 | 3.10, 3.11, 3.12 | 2.5, 2.6, 2.7, 2.8 | 12.4, 12.6, 12.8, 12.9 |

### v0.4.10

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.10)

#### Windows x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.7.4, 2.8.2 | 3.10, 3.11, 3.12 | 2.7, 2.8 | 12.8 |

### v0.4.9

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.4.9)

#### Windows x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.7.4 | 3.11 | 2.7 | 12.8 |

### v0.3.18

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.18)

#### Linux x86_64

| Flash-Attention | Python | PyTorch | CUDA |
| --- | --- | --- | --- |
| 2.7.4 | 3.10, 3.11, 3.12 | 2.5, 2.6, 2.7, 2.8 | 12.4, 12.8, 12.9 |

### v0.3.14

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.14)

#### Linux x86_64

| Flash-Attention | Python           | PyTorch                    | CUDA                   |
| --------------- | ---------------- | -------------------------- | ---------------------- |
| 2.6.3, 2.8.2    | 3.10, 3.11, 3.12 | 2.5.1, 2.6.0, 2.7.1, 2.8.0 | 12.4.1, 12.8.1, 12.9.1 |

### v0.3.13

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.13)

#### Linux x86_64

| Flash-Attention | Python           | PyTorch                    | CUDA   |
| --------------- | ---------------- | -------------------------- | ------ |
| 2.8.1           | 3.10, 3.11, 3.12 | 2.4.1, 2.5.1, 2.6.0, 2.7.1 | 12.8.1 |

### v0.3.12

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.12)

#### Linux x86_64

| Flash-Attention | Python           | PyTorch                    | CUDA           |
| --------------- | ---------------- | -------------------------- | -------------- |
| 2.8.0           | 3.10, 3.11, 3.12 | 2.4.1, 2.5.1, 2.6.0, 2.7.1 | 12.4.1, 12.8.1 |

### v0.3.10

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.10)

#### Linux x86_64

| Flash-Attention | Python           | PyTorch | CUDA   |
| --------------- | ---------------- | ------- | ------ |
| 2.7.4           | 3.10, 3.11, 3.12 | 2.7.1   | 12.8.1 |

### v0.3.9

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.9)

#### Linux x86_64

| Flash-Attention     | Python           | PyTorch | CUDA   |
| ------------------- | ---------------- | ------- | ------ |
| 2.4.3, 2.5.9, 2.6.3 | 3.10, 3.11, 3.12 | 2.7.1   | 12.8.1 |

#### Windows x86_64

| Flash-Attention     | Python           | PyTorch             | CUDA   |
| ------------------- | ---------------- | ------------------- | ------ |
| 2.5.9, 2.6.3, 2.7.4 | 3.10, 3.11, 3.12 | 2.4.1, 2.5.1, 2.6.0 | 12.4.1 |

> [!IMPORTANT]
> ⚠️ Building flash-attn v2.7.4 with CUDA 12.8 on Windows cannot be completed because of GitHub Actions’ processing-time limits. In the future, I plan to add a self-hosted Windows runner to resolve this issue.

### v0.3.1

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.3.1)

#### Windows x86_64

| Flash-Attention | Python | PyTorch | CUDA   |
| --------------- | ------ | ------- | ------ |
| 2.6.3           | 3.11   | 2.6.0   | 12.6.3 |

From this version, Wheels for Windows are released.  
However, we are waiting for a report on how it works because we have not tested it enough.

### v0.2.1

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.1)

| Flash-Attention            | Python           | PyTorch           | CUDA   |
| -------------------------- | ---------------- | ----------------- | ------ |
| 2.4.3, 2.5.9, 2.6.3, 2.7.4 | 3.10, 3.11, 3.12 | 2.8.0.dev20250523 | 12.8.1 |

### v0.2.0

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.2.0)

| Flash-Attention     | Python           | PyTorch           | CUDA   |
| ------------------- | ---------------- | ----------------- | ------ |
| 2.4.3, 2.5.9, 2.6.3 | 3.10, 3.11, 3.12 | 2.8.0.dev20250523 | 12.8.1 |

### v0.1.0

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.1.0)

| Flash-Attention            | Python           | PyTorch | CUDA   |
| -------------------------- | ---------------- | ------- | ------ |
| 2.4.3, 2.5.9, 2.6.3, 2.7.4 | 3.10, 3.11, 3.12 | 2.7.0   | 12.8.1 |

v2.7.4 and v2.7.4.post1 are the same version.

From this release, self-hosted runners are used for building some wheels.

### v0.0.9

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.9)

| Flash-Attention     | Python           | PyTorch | CUDA   |
| ------------------- | ---------------- | ------- | ------ |
| 2.4.3, 2.5.9, 2.6.3 | 3.10, 3.11, 3.12 | 2.7.0   | 12.8.1 |

### v0.0.8

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.8)

| Flash-Attention                  | Python           | PyTorch                    | CUDA                   |
| -------------------------------- | ---------------- | -------------------------- | ---------------------- |
| 2.4.3, 2.5.9, 2.6.3, 2.7.4.post1 | 3.10, 3.11, 3.12 | 2.4.1, 2.5.1, 2.6.0, 2.7.0 | 11.8.0, 12.4.1, 12.6.3 |

### v0.0.7

Skip for experimental reasons.

### v0.0.6

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.6)

| Flash-Attention                  | Python           | PyTorch                           | CUDA           |
| -------------------------------- | ---------------- | --------------------------------- | -------------- |
| 2.4.3, 2.5.9, 2.6.3, 2.7.4.post1 | 3.10, 3.11, 3.12 | 2.2.2, 2.3.1, 2.4.1, 2.5.1, 2.6.0 | 12.4.1, 12.6.3 |

### v0.0.5

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.5)

| Flash-Attention    | Python           | PyTorch                                         | CUDA           |
| ------------------ | ---------------- | ----------------------------------------------- | -------------- |
| 2.6.3, 2.7.4.post1 | 3.10, 3.11, 3.12 | 2.0.1, 2.1.2, 2.2.2, 2.3.1, 2.4.1, 2.5.1, 2.6.0 | 12.4.1, 12.6.3 |

### v0.0.4

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.4)

| Flash-Attention | Python           | PyTorch                                  | CUDA                   |
| --------------- | ---------------- | ---------------------------------------- | ---------------------- |
| 2.7.3           | 3.10, 3.11, 3.12 | 2.0.1, 2.1.2, 2.2.2, 2.3.1, 2.4.1, 2.5.1 | 11.8.0, 12.1.1, 12.4.1 |

### v0.0.3

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.3)

| Flash-Attention | Python           | PyTorch                                  | CUDA                   |
| --------------- | ---------------- | ---------------------------------------- | ---------------------- |
| 2.7.2.post1     | 3.10, 3.11, 3.12 | 2.0.1, 2.1.2, 2.2.2, 2.3.1, 2.4.1, 2.5.1 | 11.8.0, 12.1.1, 12.4.1 |

### v0.0.2

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.2)

| Flash-Attention                  | Python           | PyTorch                                  | CUDA                   |
| -------------------------------- | ---------------- | ---------------------------------------- | ---------------------- |
| 2.4.3, 2.5.6, 2.6.3, 2.7.0.post2 | 3.10, 3.11, 3.12 | 2.0.1, 2.1.2, 2.2.2, 2.3.1, 2.4.1, 2.5.1 | 11.8.0, 12.1.1, 12.4.1 |

### v0.0.1

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.1)

| flash-attention                   | Python           | PyTorch                                  | CUDA                   |
| --------------------------------- | ---------------- | ---------------------------------------- | ---------------------- |
| 1.0.9, 2.4.3, 2.5.6, 2.5.9, 2.6.3 | 3.10, 3.11, 3.12 | 2.0.1, 2.1.2, 2.2.2, 2.3.1, 2.4.1, 2.5.0 | 11.8.0, 12.1.1, 12.4.1 |

### v0.0.0

[Release](https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/tag/v0.0.0)

| flash-attention            | Python     | PyTorch                                  | CUDA                   |
| -------------------------- | ---------- | ---------------------------------------- | ---------------------- |
| 2.4.3, 2.5.6, 2.5.9, 2.6.3 | 3.11, 3.12 | 2.0.1, 2.1.2, 2.2.2, 2.3.1, 2.4.1, 2.5.0 | 11.8.0, 12.1.1, 12.4.1 |

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
