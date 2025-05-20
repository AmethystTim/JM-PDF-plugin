import asyncio

from pkg.plugin.context import EventContext
from pkg.plugin.events import * 
from pkg.platform.types import *

from ..utils.rankhandler import *

async def jmRank(ctx: EventContext, args: list, msg_platform: MsgPlatform = None) -> None:
    '''处理/jm rank'''
    duration, = args
    if not duration:
        duration = 'week'
    await ctx.reply(MessageChain([Plain("获取排行榜中，请坐和放宽")]))
    
    '''获取排行榜结果'''
    try:
        await asyncio.wait_for(rankHandler(msg_platform, ctx, duration), timeout=10)
    except asyncio.TimeoutError:
        await ctx.reply(MessageChain([Plain("获取排行榜超时，可能是网络连接问题，请稍后重试")]))