import contextlib
import json
import os
import subprocess
import sys

# ----------------------- Utility --------------------------
import traceback
from os.path import join

import click
from click import echo, style

from wiseai.utils.config import AGENT_LOG_FILE_PATH, AGENT_INFO, AGENT_CONFIG_PATH


@contextlib.contextmanager
def stdout_redirect(where):
    sys.stdout = where
    try:
        yield where
    finally:
        sys.stdout = sys.__stdout__


@contextlib.contextmanager
def stderr_redirect(where):
    sys.stderr = where
    try:
        yield where
    finally:
        sys.stderr = sys.__stderr__


def create_dir(directory):
    """
        Creates a directory if it does not exists
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


@click.command()
@click.option(
    "--agent_id",
    help="Input the credit of the WiseAgent Instance.",
    required=True,
)
def run_agent(agent_id: int):
    # log file.
    create_dir(AGENT_LOG_FILE_PATH)
    stdout_file = join(AGENT_LOG_FILE_PATH, "temp_stdout.txt")
    stderr_file = join(AGENT_LOG_FILE_PATH, "temp_stderr.txt")
    stdout = open(stdout_file, "a+")
    stderr = open(stderr_file, "a+")

    agent_config_path = AGENT_CONFIG_PATH.format(agent_id)
    if os.path.exists(agent_config_path):
        with open(agent_config_path, 'r') as f:
            config = json.load(f)
    else:
        echo(style(
            f"Cannot load agent: {agent_id} locally",
            fg='red'
        ))
        return
    agent_root = config.get('root_dir')
    agent_launch = os.path.join(agent_root, 'run.py')
    try:
        with stdout_redirect(stdout), stderr_redirect(stderr):
            subprocess.call(["python", agent_launch, "--config", agent_config_path])
    except Exception:
        stderr.write(traceback.format_exc())
        stdout.close()
        stderr.close()


if __name__ == '__main__':
    run_agent(1)
