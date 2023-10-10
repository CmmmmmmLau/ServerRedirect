import functools
import time
from typing import Union

from mcdreforged.api.decorator import new_thread
from mcdreforged.command.builder.exception import RequirementNotMet
from mcdreforged.command.builder.nodes.arguments import Text
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.command.command_source import CommandSource, PlayerCommandSource
from mcdreforged.minecraft.rtext.style import RColor, RStyle
from mcdreforged.minecraft.rtext.text import RAction, RText, RTextList
from mcdreforged.plugin.server_interface import PluginServerInterface, ServerInterface
from mcdreforged.translation.translation_text import RTextMCDRTranslation

from server_redirect import constants, serverStatusAPI


def rtr(I18nKey: str, *args, **kwargs) -> RTextMCDRTranslation:
    return ServerInterface.get_instance().rtr(f"server_redirect.{I18nKey}", *args, **kwargs)


def executeCommand(source: CommandSource, command: str):
    if source.get_server().get_mcdr_config().get("handler") == "forge_handler":
        source.get_server().execute("/" + command)
    else:
        source.get_server().execute(command)


def printHelpMessage(source: CommandSource):
    meta = constants.meta
    source.reply(rtr("help", prefix=constants.PREFIX, name=meta.name, version=meta.version))


@new_thread
def printServerList(source: Union[CommandSource, str], config: constants.ServerList):
    serverStatus = []
    serverName = []
    for key, value in config.serverList.items():
        serverConfig: constants.ServerConfig = value
        serverName.append(key)
        status: serverStatusAPI.ServerStatus = serverStatusAPI.getServerStatus(serverConfig.address, serverConfig.port)
        serverStatus.append(status)

    text = ""
    for i in range(len(serverName)):
        text += RText(f"{serverName[i]:<15}", color=RColor.yellow)
        if serverStatus[i]:
            text += RTextList(
                RText(rtr("online")),
                RText(f" {serverStatus[i].online:<2}/{serverStatus[i].max} "),
                RText(rtr("join"), color=RColor.yellow, styles=[RStyle.underlined, RStyle.bold])
                .set_click_event(RAction.run_command, f"!!server {serverName[i]}")
            )
            text += RTextList(
                RText(rtr("player_list")),
                RText(", ".join(serverStatus[i].playerList))
            )
            text += RText("\n")
        else:
            text += RText(rtr("offline"))
            text += RText("\n")

    if isinstance(source, CommandSource):
        source.reply(text)
    else:
        ServerInterface.get_instance().tell(source, text)


@new_thread
def redirectPlayer(source: CommandSource, context: dict, server: str, config: constants.ServerConfig):
    player = context["Target Player"]
    source.reply(rtr("redirect.info_1", player=player, server=server))
    source.get_server().get_instance().tell(player, rtr("redirect.info_2", server=server))
    for i in range(5, 0, -1):
        source.get_server().get_instance().tell(player, f"§e ~~~~ {i} ~~~~")
        time.sleep(1)
    executeCommand(source, f"redirect {player} {config.address}:{config.port}")


@new_thread
def selfRedirect(source: CommandSource, context: dict, config: constants.ServerList):
    if isinstance(source, PlayerCommandSource):
        target = context["Target Server"]
        if target in config.serverList:
            address = config.serverList.get(target).address
            port = config.serverList.get(target).port
            executeCommand(source, f"redirect {source.player} {address}:{port}")
        else:
            source.reply(rtr("error_1"))
    else:
        source.reply(rtr("c_only"))


def registerCommand(server: PluginServerInterface, config: constants.ServerList):
    def getLiteral(literal: str, permission: int):
        return Literal(literal).requires(lambda src: src.has_permission(permission)) \
            .on_error(RequirementNotMet, lambda src: src.reply(rtr("denied")), handled=True)

    nodeRoot = getLiteral(constants.PREFIX, 1).runs(printHelpMessage)
    nodeList = getLiteral("list", 1).runs(functools.partial(printServerList, config=config))
    nodeSelfRedirect = Text("Target Server").runs(functools.partial(selfRedirect, config=config))

    nodeRedirect = getLiteral("redirect", 3).runs(lambda src: src.reply(rtr("redirect.miss_argument")))

    for key, value in config.serverList.items():
        nodeServer = getLiteral(key, 3).runs(functools.partial(selfRedirect, server=key)) \
            .then(Text("Target Player")
                  .runs(functools.partial(redirectPlayer, server=key, config=value)))
        nodeRedirect.then(nodeServer)

    nodeReload = getLiteral("reload", 3).runs(
        lambda src: server.load_config_simple("ServerList.json", target_class=constants.ServerList))

    server.register_command(
        nodeRoot
        .then(nodeList)
        .then(nodeRedirect)
        .then(nodeSelfRedirect)
        .then(nodeReload)
    )

    server.register_help_message("!!online", rtr("help_summary"))
