# Security Policy

## Security Maintainer

Security issues for this project are coordinated by **Junya Morioka (@mjun0812)**, the project maintainer and security contact.

## Scope

Security reports are in scope when they relate to this repository or infrastructure maintained for this project, including:

- Build and release workflows.
- GitHub Actions configuration and project-maintained custom actions.
- Self-hosted runner configuration used to build release artifacts.
- AWS CodeBuild integration used by the project.
- Dependency and upstream-source handling performed by project-maintained scripts or workflows.
- Integrity, provenance, or publication of wheel artifacts released by this project.
- Vulnerabilities introduced by project-maintained code, scripts, configuration, or packaging logic.

Issues in upstream projects such as FlashAttention, PyTorch, CUDA, ROCm, or third-party dependencies should normally be reported to the relevant upstream project unless the issue specifically concerns how this repository builds, packages, or distributes them.

## Reporting a Vulnerability

Please do **not** disclose suspected vulnerabilities, exploit details, credentials, or sensitive infrastructure information in a public issue.

If GitHub's **Report a vulnerability** option is available for this repository, use it to submit the report privately.

If private vulnerability reporting is not available, open a minimal public issue titled **Security contact request** without vulnerability details. The maintainer will arrange a private channel for follow-up.

When possible, include:

- A concise description of the issue and its security impact.
- The affected workflow, script, artifact, or infrastructure component.
- Reproduction steps or a minimal proof of concept.
- Any relevant version, commit, runner, platform, CUDA/ROCm, PyTorch, or Python details.
- Suggested mitigations, if known.

## Handling

Reports will be reviewed on a best-effort basis. Confirmed vulnerabilities will be investigated, mitigated, and disclosed in a manner appropriate to their impact and to any affected upstream projects or downstream users.

Security testing must be limited to systems and infrastructure you own or are explicitly authorized to assess. Do not perform disruptive testing against shared build infrastructure or third-party systems.
