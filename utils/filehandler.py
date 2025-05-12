import os
import asyncio
import yaml

from pkg.core.entities import LauncherTypes
from pkg.plugin.context import EventContext

from ..cells.apicaller import MsgPlatform

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yml')
DOCKER_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'docker.yml')

class FileHandler:
    '''处理文件操作'''
    def __init__(self, msg_platform: MsgPlatform, ctx: EventContext, manga_id: str, chapter_id: int):
        '''
        Args:
            msg_platform (MsgPlatform): 消息平台实例
            ctx (EventContext): 事件上下文
            name (str): 文件名
        '''
        self.msg_platform = msg_platform
        self.ctx = ctx
        self.name = f"{manga_id}-{chapter_id}.pdf"
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.file = os.path.join(data["dir_rule"]["base_dir"], self.name)
        with open(DOCKER_CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if data['docker_cfg']['enabled']:
                self.file = os.path.join(data["docker_cfg"]["host_base_dir"], self.name)
    
    async def sendFile(self):
        '''发送文件'''
        match self.ctx.event.query.launcher_type:
            case LauncherTypes.PERSON:
                await self.msg_platform.callApi('/upload_private_file', {
                    'user_id': str(self.ctx.event.sender_id),
                    'file': self.file,
                    'name': self.name
                })
            case LauncherTypes.GROUP:
                await self.msg_platform.callApi('/upload_group_file', {
                    'group_id': str(self.ctx.event.launcher_id),
                    'file': self.file,
                    'name': self.name
                })
            case _:
                raise ValueError(f"Unsupported launcher type: {self.ctx.event.query.launcher_type}")
        
    async def recallFile(self, wait_time: int):
        '''撤回文件
        
        Args:
            wait_time (int): 撤回等待时间
        '''
        await asyncio.sleep(wait_time)
        
        data = await self.msg_platform.callApi("/get_group_root_files", {
            "group_id": str(self.ctx.event.launcher_id)
        })
        file_list = data.get("data", []).get("files", [])
        target_file = None
        
        for f in file_list:   # 倒序查找
            if f.get("file_name", "") == self.name:
                target_file = f
                break
        if not target_file:
            print(f"[JM PDF plugin] 文件{self.name}不存在，撤回失败")
            return
        
        await self.msg_platform.callApi("/delete_group_file", {
            "group_id": str(self.ctx.event.launcher_id),
            "file_id": target_file["file_id"],
            "busid": target_file["busid"]
        })
        
        print(f"[JM PDF plugin] 文件{self.name}撤回成功")