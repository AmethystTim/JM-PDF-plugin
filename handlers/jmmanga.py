from pkg.plugin.context import EventContext
from pkg.plugin.events import * 
from pkg.platform.types import *
from pkg.core.entities import LauncherTypes

from ..cells.converter import *
from ..cells.downloader import *

from ..utils.filehandler import *

async def jmManga(ctx: EventContext, args: list, msg_platform: MsgPlatform = None) -> None:
    '''处理/jm [ID] [CHAPTER]'''
    manga_id, chapter_id = args
    
    chapter_id = int(chapter_id) if chapter_id else 1
    if chapter_id < 0:
        await ctx.reply(MessageChain([Plain(f"章节号不能为负数")]))
        return
    
    await ctx.reply(MessageChain([Plain(f"正在将jm{manga_id}的第{chapter_id}章转换为PDF...\n可能需要10s至1min不等，请耐心等待")]))
    
    '''下载漫画'''
    downloader = Downloader(manga_id)
    status, err = downloader.downloadManga()
    if status != 0:
        await ctx.reply(MessageChain([Plain(err)]))
        return
    
    '''转换PDF'''
    converter = Converter(manga_id)
    status, err = converter.manga2Pdf(chapter_id)
    if status != 0:
        await ctx.reply(MessageChain([Plain(err)]))
        return
    
    '''发送PDF'''
    filehandler = FileHandler(msg_platform, ctx, manga_id, chapter_id)
    await filehandler.sendFile()
    
    '''撤回PDF'''
    wait_time = 20
    if ctx.event.query.launcher_type == LauncherTypes.GROUP:
        await ctx.reply(MessageChain([Plain(f"文件发送完成，{wait_time}s后自动撤回")]))
        asyncio.create_task(filehandler.recallFile(wait_time))
