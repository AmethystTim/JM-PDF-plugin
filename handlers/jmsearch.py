import asyncio

from pkg.plugin.context import EventContext
from pkg.plugin.events import * 
from pkg.platform.types import *

from ..utils.searchhandler import *

async def jmSearch(ctx: EventContext, args: list, msg_platform: MsgPlatform = None) -> None:
    '''处理/jm search [KEYWORD]'''
    keyword, = args
    
    await ctx.reply(MessageChain([Plain("获取搜索结果中，请坐和放宽")]))
    
    '''获取搜索结果'''
    try:
        await asyncio.wait_for(searchHandler(msg_platform, ctx, keyword, "site"), timeout=10)
    except asyncio.TimeoutError:
        await ctx.reply(MessageChain([Plain("搜索超时，可能是网络连接问题，请稍后重试")]))