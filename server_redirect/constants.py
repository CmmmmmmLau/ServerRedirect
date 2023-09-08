from typing import Dict

from mcdreforged.utils.serializer import Serializable

PREFIX = "!!server"


class ServerConfig(Serializable):
    address: str = "localhost"
    port: int = 25565


class ServerList(Serializable):
    serverList: Dict[str, ServerConfig] = {
        "Survival": ServerConfig(),
        "Creative": ServerConfig(port=25575)
    }

