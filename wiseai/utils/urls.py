from enum import Enum


class URLS(Enum):
    login = "/api/auth/login"
    build_agent = "/api/agent/build_agent/{}/"
    agent_list = "/api/agent/user_agent_list"
