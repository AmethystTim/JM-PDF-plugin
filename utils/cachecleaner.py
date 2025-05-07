import os
import yaml
import shutil

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yml')

class CacheCleaner:
    def __init__(self, maxfilecount=2):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.cache_dir = config['dir_rule']['base_dir']
        self.maxfilecount = maxfilecount
    
    def cleanCache(self):
        '''检查并清理缓存'''
        files = os.listdir(self.cache_dir)
        files = [f for f in files if not f.endswith(".gitkeep")]    # 忽略.gitkeep
        
        # 超过设定文件数量上限清除缓存
        if len(files) >= self.maxfilecount: 
            print(f"[JM PDF plugin] 超过设定文件数量上限，开始清除缓存")
            file_time = [{f: os.path.getmtime(os.path.join(self.cache_dir, f))} for f in files]
            file_time.sort(key=lambda x: list(x.values())[0])
            try:
                for f in file_time:
                    if os.path.isfile(os.path.join(self.cache_dir, list(f.keys())[0])):
                        os.remove(os.path.join(self.cache_dir, list(f.keys())[0]))
                    elif os.path.isdir(os.path.join(self.cache_dir, list(f.keys())[0])):
                        shutil.rmtree(os.path.join(self.cache_dir, list(f.keys())[0]))
                print(f"[JM PDF plugin] 成功清除缓存")
            except PermissionError as e:
                print(f"[JM PDF plugin] 权限错误，无法删除文件: {os.path.join(self.cache_dir, list(f.keys())[0])}. 错误信息: {e}")
            except Exception as e:
                print(f"[JM PDF plugin] 删除文件时发生未知错误: {e}")