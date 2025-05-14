import re
import os
import yaml

from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import * 
from pkg.platform.types import *
from pkg.core.entities import LauncherTypes

from .cells.apicaller import *
from .cells.converter import *
from .cells.downloader import *
from .cells.argsparser import *
from .cells.controller import *

from .utils.cachecleaner import *

from .handlers.jmmanga import *
from .handlers.jmsearch import *
from .handlers.jmclear import *

current_dir = os.path.dirname(__file__)

# 注册插件
@register(name="JM PDF plugin", description="突破卡脖子核心技术的漫画下载插件🧩", version="1.2", author="AmethystTim")
class JMPDFPlugin(BasePlugin):
    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.msg_platform = MsgPlatform(port=3000)
        self.maxfilecount = 50 # 最大缓存文件数量
        self.instructions = {
            "/jm": 
                r"^/jm(?: help)?$",
            "/jm [ID] [CHAPTER]": 
                r"^/jm (\d+)(?: (\d+))?$",
            "/jm search [KEYWORD]" : 
                r"^/jm search (.+)$",
            "/jm clear": 
                r"^/jm clear$"
        }
        
        host.ap.logger.info(f"[JM PDF plugin] 正在应用指令管理配置...")
        self.controller = Controller(self.instructions)
        self.instructions = self.controller.initConfig()
        
        host.ap.logger.info(f"[JM PDF plugin] 插件加载完成")
    
    def matchPattern(self, msg):
        '''
        匹配指令
        
        Args:
            msg (str): 指令内容
        Returns:
            res (str): 匹配结果
        '''
        res = None
        for pattern in self.instructions:
            if re.match(self.instructions[pattern], msg):
                res = pattern
        return res
    
    # 异步初始化
    async def initialize(self):
        pass

    # 当收到群/私聊消息时触发
    @handler(PersonMessageReceived)
    @handler(GroupMessageReceived)
    async def group_message_received(self, ctx: EventContext):
        msg = str(ctx.event.message_chain).strip()
        
        # 文案匹配
        if not msg.startswith("/jm") and not self.controller.checkisDisabled('[text]'):
            manga_id = "".join([char for char in msg if char.isdigit()])
            if 6 <= len(manga_id) <= 7:
                await ctx.reply(MessageChain([Plain(f"检测到jm号{manga_id}")]))
                msg = f"/jm {manga_id}"
        
        # 匹配指令
        pattern = self.matchPattern(msg)
        if not pattern:
            return
        
        # 白名单机制
        type = ctx.event.query.launcher_type
        if not self.controller.controlAccess(int(ctx.event.launcher_id), type):
            print(f"[JM PDF plugin] 白名单机制触发，{'用户' if type == LauncherTypes.PERSON else '群聊'}{ctx.event.launcher_id}无法使用该插件")
            return
        
        # 清理缓存
        cachecleaner = CacheCleaner(self.maxfilecount)
        cachecleaner.cleanCache()
        
        match pattern:
            case "/jm":
                await ctx.reply(MessageChain([
                    Plain("突破jm卡脖子核心技术\n"),
                    Plain("· 将jm号对应本子转化为pdf\n\t如：/jm 123456\n"),
                    Plain("· 指定章节转化\n\t如：/jm 123456 2\n"),
                    Plain("· jm站内搜索\n\t如：/jm search 偶像大师\n")
                ]))
            case "/jm [ID] [CHAPTER]":
                await jmManga(ctx, parseArgs(self.instructions[pattern], msg), self.msg_platform)
            case "/jm search [KEYWORD]":
                await jmSearch(ctx, parseArgs(self.instructions[pattern], msg), self.msg_platform)
            case "/jm clear":
                await jmClear(ctx, parseArgs(self.instructions[pattern], msg), self.msg_platform)
            case _:
                pass
        
    # 插件卸载时触发
    def __del__(self):
        pass
