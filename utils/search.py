import jmcomic
import os
import yaml
from plugins.JM_PDF_plugin.utils.callapi import NapCatApi
from pkg.plugin.context import EventContext

async def searchManga(napcat: NapCatApi, ctx: EventContext, search_query: str, mode: str):
    '''
    搜索漫画
    
    args:
        napcat: NapCatApi
        ctx: EventContext
        search_query: 搜索关键字
        mode: 搜索模式
    '''
    msg = '搜索结果：'
    client = None
    config_path = os.path.join(os.path.dirname(__file__), "../config.yml")
    with open(config_path, "r", encoding="utf-8") as cfg:
        config: dict = yaml.load(cfg, Loader = yaml.FullLoader)
        client = jmcomic.JmOption.default().new_jm_client(
            domain_list=config.get("client", {}).get("domain", {}).get("api", None),
            impl="api"
        )
    page = None
    match mode:
        case "site": # 站内搜索
            page: jmcomic.JmSearchPage = client.search_site(f"+{search_query}", page=1)
        case _:
            return
    for album_id, title in page:
        print(f'[{album_id}]: {title}')
        msg += f'\n[{album_id}]: {title}'
    await NapCatApi.callApi(napcat, '/send_group_forward_msg', {
        "group_id": str(ctx.event.launcher_id),
        "user_id": "",
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
        "source": "搜索结果"
    })