import jmcomic
import os
import yaml

from pkg.plugin.context import EventContext
from pkg.core.entities import LauncherTypes

from ..cells.apicaller import MsgPlatform

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yml')

async def rankHandler(msg_platform: MsgPlatform, ctx: EventContext, duration: str):
    '''
    获取漫画排行榜
    
    Args:
        msg_platform (MsgPlatform): 消息平台实例
        ctx (EventContext): 事件上下文
        duration (str): 排行榜时间范围
    '''
    msg = f"{'周' if duration == 'week' else '月'}排行榜"
    
    client = None
    with open(CONFIG_PATH, "r", encoding="utf-8") as cfg:
        config: dict = yaml.load(cfg, Loader = yaml.FullLoader)
        print(f"config: {config.get('client', {}).get('domain', {}).get('api', None)}")
        client = jmcomic.JmOption.default().new_jm_client(
            domain_list=config.get('client', {}).get('domain', {}).get('api', None),
            impl="api"
        )
    match duration:
        case "week":
            page: jmcomic.JmCategoryPage = client.week_ranking(1)
        case "month":
            page: jmcomic.JmCategoryPage = client.month_ranking(1)
        case _:
            return
    for album_id, title in page:
        msg += f'\n\n[{album_id}]: {title}'
    
    await msg_platform.callApi('/send_forward_msg', {
        "group_id": str(ctx.event.launcher_id) if ctx.event.query.launcher_type == LauncherTypes.GROUP else "",
        "user_id": str(ctx.event.query.sender_id) if ctx.event.query.launcher_type == LauncherTypes.PERSON else "",
        "messages": [
            {
                "type": "node",
                "data": {
                    "user_id": f"{ctx.event.query.sender_id}",
                    "nickname": "BOT",
                    "content": [
                        {
                            "type": "text",
                            "data": {
                                "text": f"{msg}"
                            }
                        }
                    ]
                }
            }
        ],
        "news": [
            {"text": f"樯橹灰飞烟灭"},
        ],
        "prompt": "[文件]年度学习资料.zip",
        "summary": "点击浏览",
        "source": f"{'周' if duration == 'week' else '月'}排行榜"
    })