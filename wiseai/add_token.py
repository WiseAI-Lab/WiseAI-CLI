import json
import os

import click
import validators
from click import echo, style

from wiseai.utils.config import WISEAI_DIR, AUTH_TOKEN_PATH, LEN_OF_TOKEN


@click.group(invoke_without_command=True)
@click.argument("auth_token")
def set_token(auth_token):
    """
    Configure EvalAI Token.
    """
    """
    Invoked by `wiseiai token <your_wiseai_auth_token>`.
    """
    if validators.length(auth_token, min=LEN_OF_TOKEN, max=LEN_OF_TOKEN):
        if not os.path.exists(WISEAI_DIR):
            os.makedirs(WISEAI_DIR)
        with open(AUTH_TOKEN_PATH, "w+") as fw:
            try:
                auth_token = {"token": "{}".format(auth_token)}  # noqa
                auth_token = json.dumps(auth_token)
                fw.write(auth_token)
            except (OSError, IOError) as e:
                echo(e)
            echo(
                style(
                    "Success: Authentication token is successfully set.",
                    bold=True,
                    fg="green",
                )
            )
    else:
        echo(
            style(
                "Error: Invalid Length. Enter a valid token of length: {}".format(
                    LEN_OF_TOKEN
                ),
                bold=True,
                fg="red"
            )
        )


@click.group(invoke_without_command=True)
def token():
    """
    Get the EvalAI token.
    """
    if not os.path.exists(AUTH_TOKEN_PATH):
        echo(
            style(
                "\nThe authentication token json file doesn't exist at the required path. "
                "Please download the file from the Profile section of the EvalAI webapp and "
                "place it at ~/.evalai/token.json or use evalai -t <token> to add it.\n\n",
                bold=True,
                fg="red",
            )
        )
    else:
        with open(AUTH_TOKEN_PATH, "r") as fr:
            try:
                data = fr.read()
                tokendata = json.loads(data)
                echo("Current token is {}".format(tokendata["token"]))
            except (OSError, IOError) as e:
                echo(e)
