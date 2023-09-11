import re

from mcdreforged.api.all import *

from . import commands, constants

config = constants.ServerList


def on_load(server: PluginServerInterface, old_module):
    global config
    config = server.load_config_simple("ServerList.json", target_class=constants.ServerList)
    commands.registerCommand(server, config)


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    global config
    commands.printServerList(server.get_plugin_command_source(), config)


