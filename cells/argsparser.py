import re

def parseArgs(pattern: str, msg: str) -> list:
    '''
    获取参数列表
    
    Args:
        pattern: 正则表达式，用于匹配参数列表
        msg: 要匹配的字符串
    Returns:
        参数列表
    '''
    match = re.search(pattern, msg)
    if match:
        return match.groups()
    else:
        return []