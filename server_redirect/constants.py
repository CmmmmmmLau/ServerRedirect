from typing import Dict

from mcdreforged.utils.serializer import Serializable
from mcdreforged.plugin.server_interface import ServerInterface

PREFIX = "!!server"

meta = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


class ServerConfig(Serializable):
    address: str = "localhost"
    port: int = 25565


class ServerList(Serializable):
    serverList: Dict[str, ServerConfig] = {
        "Survival": ServerConfig(),
        "Creative": ServerConfig(port=25575)
    }
