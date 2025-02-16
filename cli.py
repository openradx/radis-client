#! /usr/bin/env python3

import sys
from pathlib import Path
from shutil import copy

import typer
from adit_radis_shared import cli_helpers as helpers

helpers.PROJECT_ID = "radis_client"
helpers.ROOT_PATH = Path(__file__).resolve().parent
postgres_container_name = "radis-client-postgres-1"

app = typer.Typer()


@app.command()
def init_workspace():
    """Initialize workspace"""

    copy(f"{helpers.get_root_path()}/example.env", f"{helpers.get_root_path()}/.env")


@app.command()
def lint():
    """Lint the source code (ruff, djlint, pyright)"""

    print("Linting Python code with ruff...")
    helpers.execute_cmd("uv run ruff check .")

    print("Linting Python code with pyright...")
    helpers.execute_cmd("uv run pyright")


@app.command()
def format_code():
    """Format the source code with ruff and djlint"""

    print("Formatting Python code with ruff...")
    helpers.execute_cmd("uv run ruff format .")

    print("Sorting Python imports with ruff...")
    helpers.execute_cmd("uv run ruff check . --fix --select I")


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def test(ctx: typer.Context):
    """Run the test suite"""

    postgres_container_up = False
    result = helpers.capture_cmd("docker ps")
    for line in result.splitlines():
        if postgres_container_name in line:
            postgres_container_up = True
            break

    if not postgres_container_up:
        sys.exit("Tests need a running PostgreSQL database.\nRun 'docker compose up -d' first.")

    cmd = f"pytest {' '.join(ctx.args)}"
    helpers.execute_cmd(cmd)


if __name__ == "__main__":
    app()
