FROM mcr.microsoft.com/devcontainers/python:3.13

# Install dependency to make bash completions work
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  bash-completion \
  && rm -rf /var/lib/apt/lists/*

USER vscode
