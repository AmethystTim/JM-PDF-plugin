'''
原项目地址：https://github.com/salikx/image2pdf/
作者：salikx
'''

import os, time, yaml
from PIL import Image

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yml")

class Converter:
    '''PDF转化器'''
    def __init__(self, manga_id: str):
        '''
        Args:
            manga_id (str): 漫画ID
        '''
        self.manga_id = manga_id
    
    def checkCache(self, chapter_id: int):
        '''检查是否存在缓存
        Args:
            chapter_id (int): 章节数
        Returns:
            True: 存在缓存
            False: 不存在缓存
        '''
        path = ""
        target_name = f"{self.manga_id}-{chapter_id}.pdf"
        with open(CONFIG_PATH, "r", encoding="utf8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            path = data["dir_rule"]["base_dir"]
        
        with os.scandir(path) as entries:
            for entry in entries:
                if not entry.name == target_name:
                    continue
                
                pdf_path = os.path.join(path, target_name)
                if os.path.exists(pdf_path):
                    print(f"[JM PDF plugin] 文件：{target_name}已存在")
                    return True
        return False
    
    def manga2Pdf(self, chapter_id=1) -> tuple[int, str]:
        '''
        将目录下图片转换为pdf文件
        
        Args:
            chapter_id (int): 章节数
        '''
        save_folder = ""
        input_folder = ""
        with open(CONFIG_PATH, "r", encoding="utf8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            save_folder = data["dir_rule"]["base_dir"]
            input_folder = os.path.join(save_folder, self.manga_id)
        
        start_time = time.time()
        path = input_folder
        subdir = []
        image = []
        sources = []

        if self.checkCache(chapter_id):
            return 0, ""
        
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    subdir.append(int(entry.name))
        subdir.sort()
        subdir = [entry for entry in subdir if entry == int(chapter_id)]
        if subdir == []:
            err = f"jm{self.manga_id}的第{chapter_id}章不存在"
            print(f"[JM PDF plugin] {err}")
            return -1, err
            
        for i in subdir:
            chapter_images = []
            with os.scandir(os.path.join(path, str(i))) as entries:
                for entry in entries:
                    if entry.is_dir():
                        err = f"{os.path.join(path, str(i))}目录下不应该有目录"
                        print(f"[JM PDF plugin] {err}")
                        return -1, err
                    if entry.is_file() and entry.name.lower().endswith(('.jpg', '.jpeg')):
                        chapter_images.append(os.path.join(path, str(i), entry.name))
            
            try:    # 按文件名中的数字排序
                chapter_images.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
            except (ValueError, IndexError):
                print(f"[JM PDF plugin] 文件名格式异常，使用字符串排序")
                chapter_images.sort()
                
            image.extend(chapter_images)
        
        if not image:
            err = "未找到任何图片文件"
            print(f"[JM PDF plugin] {err}")
            return -1, err

        '''处理第一张图片并初始化output'''
        first_image = None
        if image:
            try:
                first_path = image[0]
                if os.path.splitext(first_path)[1].lower() in ['.jpg', '.jpeg']:
                    first_image = Image.open(first_path)
                    # 确保图片模式正确
                    if first_image.mode != "RGB":
                        first_image = first_image.convert("RGB")
                    output = first_image  # 设置第一张图片为输出基础
                    # 不再从列表中移除第一张图片
                else:
                    err = f"第一个文件 {first_path} 不是有效的图片文件"
                    print(f"[JM PDF plugin] {err}")
                    return -1, err
            except Exception as e:
                err = f"处理第一张图片失败: {e}"
                print(f"[JM PDF plugin] {err}")
                return -1, err
        else:
            err = "未找到有效的图片文件"
            print(f"[JM PDF plugin] {err}")
            return -1, err

        '''处理所有图片（包括第一张）'''
        for file in image:
            if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg']:
                try:
                    img_file = Image.open(file)
                    if img_file.mode != "RGB":
                        img_file = img_file.convert("RGB")
                    # 只有不是第一张图片才添加到sources列表
                    if file != image[0]:
                        sources.append(img_file)
                except Exception as e:
                    err = f"处理图片 {file} 失败: {e}"
                    print(f"[JM PDF plugin] {err}")
                    return -1, err

        pdf_file_path = os.path.join(save_folder, f"{self.manga_id}-{chapter_id}.pdf")
            
        '''保存PDF'''
        try:
            output.save(pdf_file_path, "PDF", save_all=True, append_images=sources)
        except Exception as e:
            err = f"保存 PDF 失败: {e}"
            print(f"[JM PDF plugin] {err}")
            return -1, err
        end_time = time.time()
        run_time = end_time - start_time
        print(f"[JM PDF plugin] 运行时间：{run_time:.2f} 秒")
        return 0, ""
