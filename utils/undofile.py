import asyncio
from plugins.JM_PDF_plugin.utils.callapi import NapCatApi
from pkg.plugin.context import EventContext

async def undo_file(napcat: NapCatApi, ctx: EventContext, manga_id: str, chap: str, wait_time: int):
    '''
    撤回文件
    
    args:
        nacpcat: NapCatApi实例
        ctx: EventContext实例
        manga_id: 漫画ID
        chap: 章节号
        wait_time: 撤回等待时间
    '''
    await asyncio.sleep(wait_time)
    print(f"[JM PDF plugin] 经过{wait_time}s，准备撤回")
    data = await napcat.callApi("/get_group_root_files", {"group_id": str(ctx.event.launcher_id)})
    file_list = data.get("data", []).get("files", [])
    target_file = None
    for f in file_list:   # 倒序查找
        if f.get("file_name", "") == f"{manga_id}{chap}.pdf":
            target_file = f
            break
    if not target_file:
        print(f"[JM PDF plugin] 文件{manga_id}{chap}.pdf不存在，撤回失败")
        return
    await napcat.callApi("/delete_group_file", {
        "group_id": str(ctx.event.launcher_id),
        "file_id": target_file["file_id"],
        "busid": target_file["busid"]
    })
    print(f"[JM PDF plugin] 文件{manga_id}{chap}.pdf撤回成功")