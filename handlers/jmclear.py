from pkg.plugin.context import EventContext
from pkg.plugin.events import * 
from pkg.platform.types import *

from ..cells.apicaller import MsgPlatform

from ..utils.cachecleaner import *

async def jmClear(ctx: EventContext, args: list, msg_platform: MsgPlatform = None) -> None:
    _ = args
    cachecleaner = CacheCleaner()
    cachecleaner.cleanCache()
    await ctx.reply(MessageChain([Plain('缓存清理完成')]))
    
    