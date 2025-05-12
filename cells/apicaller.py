import json
import aiohttp
import os
import yaml

DOCKER_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "docker.yml")

class MsgPlatform():
    '''消息平台类'''
    def __init__(self, port: int):
        '''
        Args:
            port (int): 端口号
        '''
        with open(DOCKER_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            host = 'host.docker.internal' if data['docker_cfg']['enabled'] else '127.0.0.1'
            self.url = f"http://{host}:{port}"

    async def callApi(self, api_url: str, payload: dict) -> dict:
        '''
        调用消息平台API
        
        Args:
            api_url (str): 发送者类型
            payload (dict): 发送内容
        Returns:
            data (dict): 返回数据
        '''
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(payload)
        async with aiohttp.ClientSession(self.url, headers=headers) as session:
            async with session.post(api_url, data=payload) as response:
                data = await response.json()
                return data