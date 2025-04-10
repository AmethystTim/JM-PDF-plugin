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
        with os.scandir(path + "/" + str(i)) as entries:
            for entry in entries:
                if entry.is_dir():
                    print(f"[JM PDF plugin] {path + "/" + str(i)}目录下不应该有目录")
                if entry.is_file():
                    image.append(path + "/" + str(i) + "/" + entry.name)

    if "jpg" in image[0]:
        output = Image.open(image[0])
        image.pop(0)

    for file in image:
        if "jpg" in file:
            img_file = Image.open(file)
            if img_file.mode == "RGB":
                img_file = img_file.convert("RGB")
            sources.append(img_file)

    pdf_file_path = pdfpath + "/" + pdfname
    if pdf_file_path.endswith(".pdf") == False:
        pdf_file_path = pdf_file_path + ".pdf"
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)
    end_time = time.time()
    run_time = end_time - start_time
    print("[JM PDF plugin] 运行时间：%3.2f 秒" % run_time)
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
    config = os.path.join(os.path.dirname(__file__), "../config.yml")
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
    config = os.path.join(os.path.dirname(__file__), "../config.yml")
    with open(config, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        path = data["dir_rule"]["base_dir"]
    with os.scandir(path) as entries:
        for entry in entries:
            if not entry.name == manga:
                continue
            if os.path.exists(os.path.join(os.path.join(path, entry.name+".pdf"))):
                print("[JM PDF plugin] 文件：《%s》 已存在，跳过" % entry.name)
                break
            else:
                print("[JM PDF plugin] 开始转换：%s " % entry.name)
                if len(os.listdir(os.path.join(path, entry.name))) > 1:
                    if all2PDF(os.path.join(path, entry.name), path, f"{entry.name}-1") == -1:
                        return -1
                else:
                    all2PDF(os.path.join(path, entry.name), path, f"{entry.name}")
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
    config = os.path.join(os.path.dirname(__file__), "../config.yml")
    with open(config, "r", encoding="utf8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        path = data["dir_rule"]["base_dir"]
        if os.path.exists(os.path.join(path, id)):
            print(f"[JM PDF plugin] 漫画{id}已存在")
            return True
        return False