import sys
from pathlib import Path
from shutil import copy

from adit_radis_shared.invoke_tasks import bump_version, lint, show_outdated  # noqa: F401
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
def publish_client(ctx: Context):
    """Publish RADIS Client to PyPI

    - Make sure PyPI API token is set: poetry config pypi-token.pypi your-api-token
    - Make sure to bump the version (see `bump_version` above)
    - Execute with `invoke publish-client`
    """
    ctx.run("poetry publish --build", pty=True)
