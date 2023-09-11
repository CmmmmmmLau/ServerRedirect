import functools

from mcdreforged.api.decorator import new_thread
from mcdreforged.command.builder.exception import RequirementNotMet
from mcdreforged.command.builder.nodes.arguments import Text
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.command.command_source import CommandSource
from mcdreforged.plugin.server_interface import PluginServerInterface, ServerInterface
from mcdreforged.translation.translation_text import RTextMCDRTranslation
from mcdreforged.minecraft.rtext.text import RAction

from . import constants


def rtr(I18nKey: str, *args, **kwargs) -> RTextMCDRTranslation:
    return ServerInterface.get_instance().as_plugin_server_interface().rtr(f"server_redirect.{I18nKey}", *args,
                                                                           **kwargs)


def printHelpMessage(source: CommandSource):
    meta = constants.meta
    source.reply(rtr("help", prefix=constants.PREFIX, name=meta.name, version=meta.version))


@new_thread
def printServerList(config: constants.ServerList):
    pass


def redirectPlayer(source:CommandSource, context: dict, server: str):
    player = context["Target Player"]
    source.reply("Redirecting player: " + player + " → " + server)
    source.get_server().as_plugin_server_interface().execute(f"list {player}")


def registerCommand(server: PluginServerInterface, config: constants.ServerList):
    def getLiteral(literal: str, permission: int):
        return Literal(literal).requires(lambda src: src.has_permission(permission)) \
            .on_error(RequirementNotMet, lambda src: src.reply("Permission Denied"), handled=True)

    nodeRoot = getLiteral(constants.PREFIX, 1).runs(printHelpMessage)
    nodeList = getLiteral("list", 1).runs(lambda src: src.reply("Hello world from list!"))

    nodeRedirect = getLiteral("redirect", 3).runs(lambda src: src.reply("Missing arguments: <Target Server> and "
                                                                        "<Target Player>"))
    for key, value in config.serverList.items():

        nodeServer = Literal(key)\
            .then(Text("Target Player").runs(functools.partial(redirectPlayer, server=key)))
        nodeRedirect.then(nodeServer)

    server.register_command(
        nodeRoot
        .then(nodeList)
        .then(nodeRedirect)
    )

    server.register_help_message("!!online", "Something here")

# TODO implement command function
