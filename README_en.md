Server Redirect 
---------

[简体中文](./README.md) | **English**

An [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) plugin for use with [Server Redirect](https://legacy.curseforge.com/minecraft/mc-mods/server-redirect) Mod in Minecraft

***
## Introduction
It is a `tool` for used with `Server Redirect` mod/plugin together.
It can allow you redirect player to other server without giving any permissions of `Server Redirect`

If you are looking for build a high version modded Minecraft(>1.12) server group. But `Waterfall` or `Velocity` not support it yet. Then here is another lightweight solution for you!

***
## Note
`Server Redirect` mod/plugin **must** be installed on both `Server` and `Client` side. This MCDReforged plugin doesn't include any proxy function for minecraft, it just can help you build a better Minecraft server group in high version of Forge/Fabric Server.

Only tested on `Spigot` 1.12.2 Server and `Forge` 1.12.2 Client.

In theory, the plugin should support all versions as long as the Server Redirect is supported.

Any problem or suggest, please Create `New issue` or `Pull request`
***
## How to use?
1. Setting up your Minecraft server as usual and go to [Server Redirect](https://legacy.curseforge.com/minecraft/mc-mods/server-redirect) page download service side mod/plugin and put it into your server folder.
2. Download this MCDReforged plugin and running it once to generate config file.
3. Modify your config to add your address and port of your server group. **Please note, it doesn't support SRV record yet.**
4. Refresh the config by using `!!server reload`, if it doesn't work then reload the plugin.
5. Login you server and testing it with `!!server list`
6. Want a cross server chat? Try this [Chat Bridge](https://github.com/TISUnion/ChatBridge)

***
## Configuration
```json
{
    "serverList": {
        "_comment": "Add your server's name here",
        "Survival": { 
            "_comment": "Add your server's address and port here",
            "address": "local",
            "port": 25565
        },
        "_comment": "repeat the same step to add another server",
        "Creative": {
            "address": "localhost",
            "port": 25575
        }
    }
}
```

***
## Commands
- `!!server`:  Display Server Redirect help information
- `!!server <Target Server>`: A client side command for player redirect himself to another server
- `!!server list`: Display the status of server group
- `!!server reload`: Reload the config file. If it doesn't work reload the plugin manual in !!MCDR plugin
- `!!server redirect <Target Server>` <Target Player>: Command for administrator to manually redirect player to another server