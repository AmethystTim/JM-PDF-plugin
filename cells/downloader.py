import os
import jmcomic
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yml")

class Downloader:
    '''漫画下载器'''
    def __init__(self, manga_id: str):
        '''
        Args:
            manga_id (str): 漫画id
        '''
        self.manga_id = manga_id

    def checkCache(self) -> bool:
        '''
        检查是否缓存漫画
        '''
        with open(CONFIG_PATH, "r", encoding="utf8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            path = data["dir_rule"]["base_dir"]
            manga_path = os.path.join(path, self.manga_id)
            if os.path.exists(manga_path):
                print(f"[JM PDF plugin] 漫画{self.manga_id}已存在")
                return True
            return False

    def downloadManga(self) -> tuple[int, str]:
        '''
        下载漫画
        '''
        loadConfig = jmcomic.JmOption.from_file(CONFIG_PATH)
        if self.checkCache():
            return 0, ""
        try:
            jmcomic.download_album(self.manga_id, loadConfig)
            return 0, ""
        except jmcomic.MissingAlbumPhotoException as e:
            err = f"id={e.error_jmid}的本子不存在或需要配置登录信息"
            print(f'[JM PDF plugin] {err}')
            return 1, err
        except jmcomic.JmcomicException as e:
            err = f'jmcomic遇到异常: {e}'
            print(f'[JM PDF plugin] {err}')
            return -1, err