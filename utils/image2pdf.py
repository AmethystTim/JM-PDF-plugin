'''
原项目地址：https://github.com/salikx/image2pdf/
作者：salikx
'''

import os, time, yaml
from PIL import Image
import jmcomic

def all2PDF(input_folder, pdfpath, pdfname, chap=1):
    '''
    将目录下图片转换为pdf文件
    
    args:
        input_folder: 输入目录
        pdfpath: pdf目录
        pdfname: pdf文件名
        chap: 章节数
    
    return: 
        0: 转换成功
        -1: 章节不存在
    '''
    start_time = time.time()
    path = input_folder
    subdir = []
    image = []
    sources = []  # pdf格式的图

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                subdir.append(int(entry.name))
    subdir.sort()
    subdir = [entry for entry in subdir if entry == int(chap)]
    if subdir == []:
        print(f"[JM PDF plugin] {chap}章不存在")
        return -1
        
    for i in subdir:
        chapter_images = []
        with os.scandir(os.path.join(path, str(i))) as entries:
            for entry in entries:
                if entry.is_dir():
                    print(f"[JM PDF plugin] {os.path.join(path, str(i))}目录下不应该有目录")
                if entry.is_file() and entry.name.lower().endswith(('.jpg', '.jpeg')):
                    chapter_images.append(os.path.join(path, str(i), entry.name))
        
        # 按文件名中的数字排序
        try:
            chapter_images.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
        except (ValueError, IndexError):
            print(f"[JM PDF plugin] 文件名格式异常，使用字符串排序")
            chapter_images.sort()
            
        image.extend(chapter_images)
    
    # 确保有图片可处理
    if not image:
        print(f"[JM PDF plugin] 未找到任何图片文件")
        return -1

    # 修复：处理第一张图片并初始化output
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
                print(f"[JM PDF plugin] 第一个文件 {first_path} 不是有效的图片文件")
                return -1
        except Exception as e:
            print(f"[JM PDF plugin] 处理第一张图片失败: {e}")
            return -1
    else:
        print(f"[JM PDF plugin] 未找到有效的图片文件")
        return -1

    # 处理所有图片（包括第一张）
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
                print(f"[JM PDF plugin] 处理图片 {file} 失败: {e}")

    # 确保PDF路径正确
    pdf_file_path = os.path.join(pdfpath, pdfname)
    if not pdf_file_path.endswith(".pdf"):
        pdf_file_path = pdf_file_path + ".pdf"
        
    # 保存PDF
    try:
        output.save(pdf_file_path, "PDF", save_all=True, append_images=sources)
    except Exception as e:
        print(f"[JM PDF plugin] 保存 PDF 时出错: {e}")
        return -1
    end_time = time.time()
    run_time = end_time - start_time
    print(f"[JM PDF plugin] 运行时间：{run_time:.2f} 秒")
    return 0


def downloadManga(manga):
    '''
    下载漫画
    
    args:
        manga: 漫画id
        
    return: 
        0: 下载成功
        1: 漫画不存在
        -1: 下载失败
    '''
    config = os.path.join(os.path.dirname(__file__), "..", "config.yml")
    loadConfig = jmcomic.JmOption.from_file(config)
    mangaCache(manga)
    try:
        jmcomic.download_album(manga, loadConfig)
        return 0
    except jmcomic.MissingAlbumPhotoException as e:
        print(f'[JM PDF plugin] id={e.error_jmid}的本子不存在')
        return 1
    except jmcomic.JmcomicException as e:
        print(f'[JM PDF plugin] jmcomic遇到异常: {e}')
        return -1

def convertPDF(manga):
    '''
    转换pdf文件
    
    args:
        manga: 漫画id
        
    return: 
        1: 存在多p
        None: 未分多p
    '''
    config = os.path.join(os.path.dirname(__file__), "..", "config.yml")
    with open(config, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        path = data["dir_rule"]["base_dir"]
    
    with os.scandir(path) as entries:
        for entry in entries:
            if not entry.name == manga:
                continue
                
            pdf_path = os.path.join(path, entry.name + ".pdf")
            if os.path.exists(pdf_path):
                print(f"[JM PDF plugin] 文件：《{entry.name}》 已存在，跳过")
                break
            else:
                print(f"[JM PDF plugin] 开始转换：{entry.name}")
                manga_path = os.path.join(path, entry.name)
                
                if len(os.listdir(manga_path)) > 1:
                    if all2PDF(manga_path, path, f"{entry.name}-1") == -1:
                        return -1
                else:
                    all2PDF(manga_path, path, entry.name)
                    
            if len(os.listdir(os.path.join(path, entry.name))) > 1:
                return 1
    return None        

def mangaCache(id):
    '''
    检查是否缓存漫画
    
    args:
        id: 漫画id
        
    return: 
        True: 已缓存
        False: 未缓存
    '''
    config = os.path.join(os.path.dirname(__file__), "..", "config.yml")
    with open(config, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        path = data["dir_rule"]["base_dir"]
        manga_path = os.path.join(path, id)
        if os.path.exists(manga_path):
            print(f"[JM PDF plugin] 漫画{id}已存在")
            return True
        return False