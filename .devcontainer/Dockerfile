FROM mcr.microsoft.com/devcontainers/python:3.13

# Install dependency to make bash completion work with invoke
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  bash-completion \
  && rm -rf /var/lib/apt/lists/*

USER vscode

# pipx is already installed in the base devcontainers Python image
RUN pipx install invoke \
  && invoke --print-completion-script=bash >> ~/.bash_completion

RUN pipx install poetry \
  && pipx inject poetry "poetry-dynamic-versioning[plugin]" \
  && poetry completions bash >> ~/.bash_completion
