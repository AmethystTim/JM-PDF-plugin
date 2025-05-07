import os
import yaml
import json

from pkg.core.entities import LauncherTypes

COMMANDS_PATH = os.path.join(os.path.dirname(__file__), "..", "commands.yml")

class Controller:
    def __init__(self, instructions: dict):
        '''
        Args:
            instructions (dict): 指令集
        '''
        self.instructions = instructions
        self.enabled_whitelist = False
        self.commands = []
        self.whitelist_groups = []
        self.whitelist_users = []
    
    def initConfig(self):
        '''初始化配置'''
        with open(COMMANDS_PATH, "r", encoding="utf-8") as f:
            '''加载配置'''
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.commands = config.get("commands", [])
            whitelist = config.get("whitelist", {})
            
            '''打印信息'''
            print(json.dumps(self.commands, indent=4))
            print(f"[JM PDF plugin] 白名单机制是否启用: {whitelist.get('enabled', False)}")
            if whitelist.get("enabled", False):
                print(f"[JM PDF plugin] 白名单中的群聊: {whitelist.get('groups', [])}")
                print(f"[JM PDF plugin] 白名单中的用户: {whitelist.get('users', [])}")
            
            '''禁用指令'''
            for command_dict in self.commands:
                command = list(command_dict.keys())[0]
                enabled = list(command_dict.values())[0]
                if not enabled and self.instructions.get(command, None):
                    self.instructions[command] = r"^\s\S" 
                    
            '''加载白名单'''        
            self.enabled_whitelist = whitelist.get("enabled", False)
            self.whitelist_groups = whitelist.get("groups", [])
            self.whitelist_users = whitelist.get("users", [])
            
        return self.instructions
    
    def controlAccess(self, id: int, launcher_type: LauncherTypes = LauncherTypes.GROUP):
        '''控制群聊的访问权限'''
        if not self.enabled_whitelist:
            return True
        else:
            match launcher_type:
                case LauncherTypes.PERSON:
                    return id in self.whitelist_users
                case LauncherTypes.GROUP:
                    return id in self.whitelist_groups
                case _:
                    return False
                
    def checkisDisabled(self, command: str):
        '''检查指令是否被禁用'''
        c = [item for item in self.commands if list(item.keys())[0] == command]
        if not c:
            return True
        else:
            if not c[0][command]:
                print(f"[JM PDF plugin] {command} 命令已被禁用")
                return True 
            return False