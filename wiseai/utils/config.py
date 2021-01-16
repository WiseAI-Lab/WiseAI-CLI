# all agent and behaviours will be stored in temp directory
import logging
import os
from os.path import expanduser

WISEAI_DIR = expanduser("~/.wiseai/")
AUTH_TOKEN_FILE_NAME = "token.json"
AUTH_TOKEN_PATH = os.path.join(WISEAI_DIR, AUTH_TOKEN_FILE_NAME)
LEN_OF_TOKEN = 41

HOST_URL_FILE_NAME = "host_url"
AGENT_LOG_FILE_NAME = "wise_agent_log"
API_HOST_URL = os.environ.get("WISEAI_API_URL", "http://localhost:8000")  # TODO: Set here.
HOST_URL_FILE_PATH = os.path.join(WISEAI_DIR, HOST_URL_FILE_NAME)
AGENT_LOG_FILE_PATH = os.path.join(WISEAI_DIR, AGENT_LOG_FILE_NAME)

AGENT_INFO = os.path.join(WISEAI_DIR, "wise_agent_{}")
DEFAULT_AGENT_ROOT_PATH = expanduser("~/wise_agent_{}")  # Take the `id` here.

AGENT_CONFIG_PATH = os.path.join(AGENT_INFO, "agent_config.json")
logger = logging.getLogger(__name__)

# web server.
SERVER_PORT = os.environ.get("DJANGO_SERVER_PORT", "8000")

AGENT_SCRIPTS = {}
BEHAVIOUR_SCRIPTS = {}

WISEAI_ERROR_CODES = [400, 401, 403, 406]
