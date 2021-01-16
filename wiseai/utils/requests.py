import json
import os
import subprocess
import zipfile

import requests
import sys
from click import echo, style

from wiseai.utils.auth import get_host_url, get_request_header
from wiseai.utils.config import WISEAI_ERROR_CODES


def validate_credit(response):
    """
    Function to check if the authentication token provided by user is valid or not.
    """
    if "detail" in response:
        if response["detail"] == "Invalid Credit":
            echo(
                style(
                    "\nThe authentication credit you are using isn't valid."
                    " Please generate it again.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
        if response["detail"] == "Credit has expired":
            echo(
                style(
                    "\nSorry, the credit has expired. Please generate it again.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)


def make_request(path, method, files=None, data=None):
    url = "{}{}".format(get_host_url(), path)
    headers = get_request_header()
    # To load an Agent by the credit, so define the `path` here.
    if method == "GET":
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code in WISEAI_ERROR_CODES:
                validate_credit(response.json())
                echo(
                    style(
                        "\nError: {}\n".format(response.json().get("error")),
                        fg="red",
                        bold=True,
                    )
                )
            else:
                echo(err)
            sys.exit(1)
        except requests.exceptions.RequestException:
            echo(
                style(
                    "\nCould not establish a connection to WiseAI."
                    " Please check the Host URL.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
        return response.json()
    elif method == "POST":
        if files:
            files = {"input_file": open(files, "rb")}
        else:
            files = None
        try:
            response = requests.post(
                url, headers=headers, files=files, data=data
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code in WISEAI_ERROR_CODES:
                validate_credit(response.json())
                echo(
                    style(
                        "\nError: {}\n",
                        fg="red",
                        bold=True,
                    )
                )
            else:
                echo(err)
            sys.exit(1)
        except requests.exceptions.RequestException:
            echo(
                style(
                    "\nCould not establish a connection to WiseAI."
                    " Please check the Host URL.\n",
                    bold=True,
                    fg="red",
                )
            )
            sys.exit(1)
        response = json.loads(response.text)
        echo(
            style(
                "\nYour Agent is successfully submitted.\n",
                fg="green",
                bold=True,
            )
        )
        return response
    elif method == "PUT":
        # TODO: Add support for PUT request
        try:
            response = requests.put(url=url, headers=headers, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            echo(
                "The worker is not able to establish connection with WiseAI due to {}"
                % (response.json())
            )
            raise
        except requests.exceptions.HTTPError:
            echo(
                f"The request to URL {url} is failed due to {response.json()}"
            )
            raise
        return response.json()
    elif method == "PATCH":
        try:
            response = requests.patch(url=url, headers=headers, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            echo(
                "The worker is not able to establish connection with WiseAI"
            )
            raise
        except requests.exceptions.HTTPError:
            echo(
                f"The request to URL {url} is failed due to {response.json()}"
            )
            raise
        return response.json()
    elif method == "DELETE":
        # TODO: Add support for DELETE request
        pass


def clone_by_git(request_url, download_location, *args):
    try:
        subprocess.check_output(['git', 'clone', request_url, download_location, *args], shell=True)
    except:
        echo(style(
            f"> git clone {request_url, download_location, *args}"
            "Unexpected error: when clone from the repository in github.\n"
            "Please check your Network or github setting in WiseAI webapp.",
            fg="red"
        ))
        exit()


def download_and_extract_file(url: str, download_location: str):
    """
    Function to extract download a file.

    Args:
        url: str, Get from 'url' by 'requests'.
        download_location: str,  It should include name of file as well.

    Returns:

    """
    try:
        response = requests.get(url)
    except Exception as e:
        echo(
            style(
                "Failed to fetch file from {}, error {}".format(url, e),
                fg="red",
                bold=True,
            )
        )
        response = None

    if response and response.status_code == 200:
        with open(download_location, "wb") as f:
            f.write(response.content)


def download_and_extract_zip_file(request_url: str, download_location: str, extract_location: str):
    """
    Function to extract download a zip file, extract it and then removes the zip file.

    Args:
        request_url: str, Get from 'url' by 'requests'.
        download_location: str, It should include name of file as well.
        extract_location: str, Store the file.

    Returns:

    """
    try:
        response = requests.get(request_url)
    except Exception as e:
        echo(
            style(
                "Failed to fetch file from {}, error {}".format(request_url, e),
                fg="red",
                bold=True,
            ))
        response = None

    if response and response.status_code == 200:
        with open(download_location, "wb") as f:
            f.write(response.content)
        # extract zip file
        zip_ref = zipfile.ZipFile(download_location, "r")
        zip_ref.extractall(extract_location)
        zip_ref.close()
        # delete zip file
        try:
            os.remove(download_location)
        except Exception as e:
            echo(
                style(
                    "Failed to remove zip file {}, error {}".format(download_location, e),
                    fg="red",
                    bold=True,
                )
            )
