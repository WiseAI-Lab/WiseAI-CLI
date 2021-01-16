"""

"""
import click
from click import echo
from .build_agent import build
from .add_token import set_token, token
from .agent_list import ps
from .set_host import host
from .login import login


@click.version_option()
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """

    """
    # agent_id: int, credit: str
    """
       Welcome to the WiseAI CLI.
       """
    if ctx.invoked_subcommand is None:
        welcome_text = (
            """
                        #######                  ###      ###    #######
                        ##      ##   ##   #####  ###     #####     ###
                        #####    ## ##   ##  ##  ###    ##   ##    ###
                        ##        ###   ###  ##  #####  #######    ###
                        #######    #     ### ### #####  ##   ##  #######\n\n"""
            "Welcome to the WiseAI CLI. Use wiseai --help for viewing all the options\n"
        )
        echo(welcome_text)


main.add_command(login)
main.add_command(set_token)
main.add_command(token)
main.add_command(host)
main.add_command(build)
main.add_command(ps)
