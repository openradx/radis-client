import sys
from pathlib import Path
from shutil import copy
from typing import Literal

from invoke.context import Context
from invoke.tasks import task

project_dir = Path(__file__).resolve().parent


###
# Helper functions
###


def check_container_up(ctx: Context, container_name):
    result = ctx.run("docker ps", hide=True, warn=True)
    assert result and result.ok
    for line in result.stdout.splitlines():
        if container_name in line:
            return True
    return False


###
# Tasks
###


@task
def init_workspace(ctx: Context):
    """Initialize workspace"""
    copy(f"{project_dir}/example.env", f"{project_dir}/.env")


@task
def lint(ctx: Context):
    """Lint the source code (ruff, pyright)"""
    cmd_ruff = "poetry run ruff check ."
    ctx.run(cmd_ruff, pty=True)
    cmd_pyright = "poetry run pyright"
    ctx.run(cmd_pyright, pty=True)


@task
def test(
    ctx: Context,
    path: str | None = None,
    cov: bool | str = False,
    html: bool = False,
    keyword: str | None = None,
    mark: str | None = None,
    stdout: bool = False,
    failfast: bool = False,
):
    """Run the test suite"""
    if not check_container_up(ctx, "postgres"):
        sys.exit("Tests need a running PostgreSQL database.\nRun 'docker compose up -d' first.")

    cmd = "pytest "
    if cov:
        cmd += "--cov "
        if isinstance(cov, str):
            cmd += f"={cov} "
        if html:
            cmd += "--cov-report=html"
    if keyword:
        cmd += f"-k {keyword} "
    if mark:
        cmd += f"-m {mark} "
    if stdout:
        cmd += "-s "
    if failfast:
        cmd += "-x "
    if path:
        cmd += path
    ctx.run(cmd, pty=True)


@task
def ci(ctx: Context):
    """Run the continuous integration (linting and tests)"""
    lint(ctx)
    test(ctx, cov=True)


@task
def bump_version(ctx: Context, rule: Literal["patch", "minor", "major"]):
    """Bump version, create a tag, commit and push to GitHub"""
    result = ctx.run("git status --porcelain", hide=True, pty=True)
    assert result and result.ok
    if result.stdout.strip():
        print("There are uncommitted changes. Aborting.")
        sys.exit(1)

    ctx.run(f"poetry version {rule}", pty=True)
    ctx.run("git add pyproject.toml", pty=True)
    ctx.run("git commit -m 'Bump version'", pty=True)
    ctx.run('git tag -a v$(poetry version -s) -m "Release v$(poetry version -s)"', pty=True)
    ctx.run("git push --follow-tags", pty=True)


@task
def publish_client(ctx: Context):
    """Publish RADIS Client to PyPI

    - Make sure PyPI API token is set: poetry config pypi-token.pypi your-api-token
    - Make sure to bump the version (see `bump_version` above)
    - Execute with `invoke publish-client`
    """
    ctx.run("poetry publish --build", pty=True)


@task
def show_outdated(ctx: Context):
    """Show outdated dependencies"""
    print("### Outdated Python dependencies ###")
    poetry_cmd = "poetry show --outdated --top-level"
    result = ctx.run(poetry_cmd, pty=True)
    assert result and result.ok
    print(result.stderr.strip())
