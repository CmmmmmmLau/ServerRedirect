Server Redirect 
---------

**简体中文** | [English](./README_en.md)

一个用来与 [Server Redirect](https://legacy.curseforge.com/minecraft/mc-mods/server-redirect) 模组/插件 配合使用的[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)插件.

***
## 介绍
该插件必须要与 `Server Redirect` 模组/插件共同使用. 这个插件能够在不给予玩家任何 `Server Redirect` 指令权限的情况下让其跳转到任务服务器.

如果你想要搭建一个高版本(>1.12.2)的模组服, 但却又因为`Waterfall` 和 `Velocity` 又不支持, 那么这个插件是一个轻量化的解决方案.

***
## 重要事项
`Server Redirect` 模组/插件 **必须** 要同时安装在 `服务端` 和 `客户端`. 这只是一个 MCDReforged 插件因此不提供任何服务器代理功能, 它只是一个帮助你实现高版本模组服群组进行跨服的一个轻量化方案.

仅在 `Spigot` 1.12.2 服务端和 `Forge` 1.12.2 客户端中进行过测试.

理论上只要 `Server Redirect` 支持的版本这个插件就能工作.

任何问题或者建议请提交 `issue` 或 `Pull request`
***
## 食用教程
1. 像往常一下先把Minecraft服务器跑起来然后去 [Server Redirect](https://legacy.curseforge.com/minecraft/mc-mods/server-redirect) 下载对应的服务端 模组/插件 并放入对应文件夹内.
2. 下载该插件并运行一次以便生成配置文件.
3. 修改这个配置文件, 并将你的服务器地址和端口填进去. **目前暂时还不支持 SRV 记录.**
4. 通过 `!!server reload` 来刷新配置文件, 没有刷新成功就手动重载插件.
5. 启动游戏登入你的服务器然后使用 `!!server list` 来进行测试.
6. 想要跨服聊天请使用该插件: [Chat Bridge](https://github.com/TISUnion/ChatBridge)

***
## Configuration
```json
{
    "serverList": {
        "_comment": "这里是你的服务器名字",
        "Survival": { 
            "_comment": "添加地址与端口",
            "address": "local",
            "port": 25565
        },
        "_comment": "要添加多个服务器,重复步骤即可",
        "Creative": {
            "address": "localhost",
            "port": 25575
        }
    }
}
```

***
## Commands
- `!!server`:  显示该插件的帮助信息.
- `!!server <Target Server>`: 只能由客户端发起的指令, 将玩家自己转发到指定服务器.
- `!!server list`: 显示服务器群组的状态.
- `!!server reload`: 重载配置文件. 如果不起效请通过 !!MCDR plugin 手动重载插件
- `!!server redirect <Target Server>` <Target Player>: 管理员权限的指令, 将玩家转发到指定的服务器