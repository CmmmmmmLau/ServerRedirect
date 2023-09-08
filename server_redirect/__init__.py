import re

from mcdreforged.api.all import *

from . import commands, constants, serverStatusAPI

config = constants.ServerList


def on_load(server: PluginServerInterface, old_module):
    global config
    config = server.load_config_simple("ServerList.json", target_class=constants.ServerList)
    commands.registerCommand(server, config)


def on_unload(server: PluginServerInterface):
    """
	Do some clean up when your plugin is being unloaded. Note that it might be a reload
	"""
    server.logger.info('Bye')


def on_info(server: PluginServerInterface, info: Info):
    """
	Handler for general server output event
	Recommend to use on_user_info instead if you only care about info created by users
	"""
    if not info.is_user and re.fullmatch(r'Starting Minecraft server on \S*', info.content):
        server.logger.info('Minecraft is starting at address {}'.format(info.content.rsplit(' ', 1)[1]))


def on_user_info(server: PluginServerInterface, info: Info):
    """
	Reacting to user input
	"""
    if info.content == '!!example':
        server.reply(info, 'example!!')


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    """
	A new player joined game, welcome!
	"""
    server.tell(player, 'Hi!')
    server.say('Welcome {}'.format(player))


def on_player_left(server: PluginServerInterface, player: str):
    """
	A player left the game, do some cleanup!
	"""
    server.say('Bye {}'.format(player))


def on_server_start(server: PluginServerInterface):
    """
	When the server begins to start
	"""
    server.logger.info('Server is starting')


def on_server_startup(server: PluginServerInterface):
    """
	When the server is fully startup
	"""
    server.logger.info('Server has started')


def on_server_stop(server: PluginServerInterface, return_code: int):
    """
	When the server process is stopped, go do some clean up
	If the server is not stopped by a plugin, this is the only chance for plugins to restart the server, otherwise MCDR
	will exit too
	"""
    server.logger.info('Server has stopped and its return code is {}'.format(return_code))


def on_mcdr_start(server: PluginServerInterface):
    """
	When MCDR just launched
	"""
    server.logger.info('Another new launch for MCDR')


def on_mcdr_stop(server: PluginServerInterface):
    """
	When MCDR is about to stop, go do some clean up
	MCDR will wait until all on_mcdr_stop event call are finished before exiting
	"""
    server.logger.info('See you next time~')
