import click
from click import echo, style

from wiseai.utils.requests import make_request

from wiseai.utils.urls import URLS


@click.command()
def ps():
    request_url = URLS.agent_list.value
    repositories = make_request(request_url, "GET")
    print_str = "------------------------ \n" \
                "- | id | name | status | \n"
    for repo in repositories:
        agents = repo.get('topics')
        for a_id, a_info in agents.items():
            name = a_info.get("name")
            status = a_info.get("status")
            print_str += f"- | {a_id} | {name} | {status} |\n"
    echo(
        style(
            print_str,
            bold=True,
            fg="black",
        )
    )
