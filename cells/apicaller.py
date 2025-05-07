import json
import aiohttp

class MsgPlatform():
    '''消息平台类'''
    def __init__(self, host: str, port: int):
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