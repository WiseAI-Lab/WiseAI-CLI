import json
import os
import stat
from typing import Dict, List, Any
from os.path import join
import shutil
import click
from click import echo, style

from wiseai.utils.config import (
    BEHAVIOUR_SCRIPTS, DEFAULT_AGENT_ROOT_PATH, WISEAI_DIR, AGENT_INFO, AGENT_CONFIG_PATH,
)
from wiseai.utils.requests import make_request, download_and_extract_zip_file, clone_by_git
from wiseai.utils.urls import URLS


def create_dir(directory):
    """
        Creates a directory if it does not exists
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_dir_as_python_package(directory: str):
    """
    Create a directory and then makes it a python
    package by creating `__init__.py` file.

    Args:
        directory: str

    Returns:

    """
    create_dir(directory)
    init_file_path = join(directory, "__init__.py")
    with open(init_file_path, "w") as init_file:  # noqa
        # to create empty file
        pass


# ---------------------- Generate agent----------------------------
def load_agent(root_path: str, agent_info: Dict):
    """
    Load a agent file from url.
    Args:
        root_path:
        agent_info:

    Returns:

    """
    # 1.Check the store_type
    store_type = agent_info.get("store_type")
    # 2. Confirm the request url
    request_url = agent_info.get('url')  # Topic's url
    extract_location = root_path

    if store_type == "zip":  # Use request
        # 3. Define the  default WiseAgent config directory by repository and topic
        repository_info = agent_info.get("repository")
        owner_name = repository_info.get("owner").get("name")  # owner
        repository_name = repository_info.get("name")  # repository
        topic_name = agent_info.get("name")  # topic
        identify = f"{owner_name}_{repository_name}_{topic_name}.zip"
        download_location = os.path.join(WISEAI_DIR, identify)
        # 4. Create the package here
        create_dir_as_python_package(extract_location)
        # 5. Download and place the WiseAgent.
        download_and_extract_zip_file(request_url=request_url,
                                      download_location=download_location,
                                      extract_location=extract_location)
    elif store_type == "git":
        clone_by_git(request_url, root_path)
    else:
        raise ValueError("Unknown Format in StoreType.")


def load_behaviours(root_path, agent_info: Dict):
    """
    Download and place the behaviours to correct path.
    Args:
        root_path:
        agent_info:

    Returns:

    """
    behaviours: List[Dict[str, Any]] = agent_info.get('behaviours')
    new_behaviours: Dict[str, Dict[str, Any]] = {}
    for behaviour in behaviours:
        try:
            store_type = behaviour.get("store_type")
            # Confirm placement
            # category ==> E.g: 'transport/mq/mqtt'
            # from {root_path}/behaviours/{category}/{behaviour_name}/behaviour import {behaviour_name}
            category = behaviour.get("category")
            # behaviour_name ==> {RepositoryName}_{TopicName}
            behaviour_name = behaviour.get("name")
            repo_name = behaviour_name.split("_")[0]
            request_url = behaviour.get("url")
            category_path = f"{root_path}/wise_agent/behaviours/{category.replace('.', '/')}"
            if not os.path.exists(category_path):
                create_dir_as_python_package(category_path)
            extract_location = os.path.join(category_path, behaviour_name)
            if store_type == "zip":  # Use request
                identify = f"{behaviour_name}.zip"
                download_location = os.path.join(WISEAI_DIR, identify)
                # 4. Create the package here
                create_dir_as_python_package(extract_location)
                # 5. Download and place the WiseAgent.
                download_and_extract_zip_file(request_url=request_url,
                                              download_location=download_location,
                                              extract_location=extract_location)
            elif store_type == "git":
                clone_by_git(request_url, extract_location)
            else:
                raise ValueError("Unknown Format in StoreType.")
            # 3. store it.
            import_path = f"{category}.{behaviour_name}.behaviour"  # all class name should be repo_name
            behaviour["import_path"] = import_path
            new_behaviours[repo_name] = behaviour
        except Exception:
            echo(
                style(
                    "Exception raised while creating Python module for behaviour_name: %s"
                    % behaviour_name,
                    fg="red"
                )
            )
            raise
        agent_info["behaviours"] = new_behaviours
        return agent_info


def readonly_handler(func, path, execinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


# ----------------------- Main ----------------------------------


# @click.command()
# @click.option(
#     "--agent_id",
#     help="Input the ID of the WiseAgent Instance.",
#     required=True,
# )
# @click.option(
#     "-p",
#     "--root_path",
#     help="The path, which is the root of build file.",
#     required=False,
# )
def build(agent_id: int, root_path: str = None):
    """
    Build an Agent in current machine.
    Args:
        agent_id:
        root_path:

    Returns:

    """
    # 1. Check Login or Not
    echo("Build...")
    # Make the basic directory.
    if root_path is None:
        root_path = DEFAULT_AGENT_ROOT_PATH.format(agent_id)
    # 2. Get the agent config by id and credit
    build_agent_path = URLS.build_agent.value
    agent_info = make_request(build_agent_path.format(agent_id), "GET")
    # 3. Load Agent
    if os.path.exists(root_path):
        shutil.rmtree(root_path, onerror=readonly_handler)
        print(f"Delete existed {root_path}")
    load_agent(root_path, agent_info)
    # 4. Load Behaviours
    agent_info = load_behaviours(root_path, agent_info)
    # 5. Save
    try:
        agent_info['root_dir'] = root_path
        agent_info_dir = AGENT_INFO.format(agent_id)
        create_dir(agent_info_dir)

        config_path = AGENT_CONFIG_PATH.format(agent_id)
        agent_info['config_path'] = config_path
        with open(config_path, 'w') as f:
            json.dump(agent_info, f)
    except IOError as e:
        echo(
            style(
                "{}".format(e),
                fg="red"
            )
        )
        return
    echo("Successfully build Agent to {}".format(root_path))
    echo("Run `wiseai ps` to check your agent.")
    # Over


if __name__ == '__main__':
    build(1)
