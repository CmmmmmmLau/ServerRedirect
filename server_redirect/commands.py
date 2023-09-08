from mcdreforged.command.builder.exception import RequirementNotMet
from mcdreforged.command.builder.nodes.arguments import Text
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.plugin.server_interface import PluginServerInterface

from . import constants


def registerCommand(server: PluginServerInterface, config: constants.ServerList):
    def getLiteral(literal: str, permission: int):
        return Literal(literal).requires(lambda src: src.has_permission(permission)) \
            .on_error(RequirementNotMet, lambda src: src.reply("Permission Denied"), handled=True)

    nodeRoot = getLiteral(constants.PREFIX, 1)
    nodeList = getLiteral("list", 1).runs(lambda src: src.reply("Hello world from list!"))
    nodeRedirect = getLiteral("redirect", 3).runs(lambda src: src.reply("Redirect!"))

    for key, value in config.serverList.items():
        nodeServer = Literal(key).then(Text("Target Player"))
        nodeRedirect.then(nodeServer)

    server.register_command(
        nodeRoot
        .then(nodeList)
        .then(nodeRedirect)
    )

# TODO implement command function
