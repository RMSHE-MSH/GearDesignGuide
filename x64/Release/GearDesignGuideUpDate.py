import requests
import os
import sys
from time import sleep

print("GearDesignGuideUpDate - Powered by RMSHE\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77'
}

Module = {
    "GearDesignGuide.exe": "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/",
    "GearDesignGuide.dll": "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/",
}

UpDateInfo_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/GDGUpDateInfo.ini?inline=false"
GDGUpDateInfo_Path = "./GDGUpDateInfo.ini"
GDGUpDateInfo_OldDate = ["GearDesignGuide.exe.2022.10.26.Mark0", "GearDesignGuide.dll.2022.10.26.Mark0", "Resource.2022.10.26.Mark0"]
GDGUpDateInfo_NewDate = ["GearDesignGuide.exe.2022.10.26.Mark0", "GearDesignGuide.dll.2022.10.26.Mark0", "Resource.2022.10.26.Mark0"]

Resource_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/Resource/"
Resource = (
    "P203_10-1.png", "P205_10-2.png", "P207_10-3.png", "P208_10-4.png", "P213_10-6.png", "P216_10-7.png",
    "P216_10-8.png", "P218_10-18.png", "P218_10-19.png", "P219_10-20.png", "P221_10-21.png"
)


def DownloadModule(URL: str, file_name: str, file_path: str):
    sleep(2)
    print(f"[提示]正在下载组件({file_name})")

    rf = requests.get(URL,  headers)
    if (rf.status_code != 200):
        print(f"[错误]无法访问服务器({URL} / {rf})")
        return False

    with open(file_path, "wb") as code:
        code.write(rf.content)
    rf.close()

    if (os.path.exists(file_path) == False):
        print(f"[错误]组件下载失败({file_path})")
        return False
    else:
        print(f"[提示]组件已下载({file_path})")
        return True


# 删除指定目录path_file下所有文件
def del_files(path_file):
    ls = os.listdir(path_file)
    for i in ls:
        f_path = os.path.join(path_file, i)
        # 判断是否是一个目录,若是,则递归删除
        if os.path.isdir(f_path):
            del_files(f_path)
        else:
            os.remove(f_path)


# 读取ini文件;
def Read_ini(file_path: str):
    # Open file
    fileHandler = open(file_path,  "r")
    # Get list of all lines in file
    listOfLines = fileHandler.readlines()
    # Close file
    fileHandler.close()

    return listOfLines


# 更新UpDateInfo(更新信息),并检查那些组件需要更新
if (os.path.exists('GDGUpDateInfo.ini') == True):
    # 读取旧的组件版本信息
    listOfLines = Read_ini(GDGUpDateInfo_Path)
    GDGUpDateInfo_OldDate.clear()
    for line in listOfLines:
        OldUpDate = line.strip()
        GDGUpDateInfo_OldDate.append(OldUpDate)

    # 删除旧的组件版本信息
    os.remove('GDGUpDateInfo.ini')

# 如果GDGUpDateInfo.ini下载成功,则开始检测那些组件需要更新
if (DownloadModule(UpDateInfo_URL, "GDGUpDateInfo.ini", GDGUpDateInfo_Path) == True):
    listOfLines = Read_ini(GDGUpDateInfo_Path)

    # 对比新旧组件版本信息
    GDGUpDateInfo_NewDate.clear()
    for line in listOfLines:
        UpDate = line.strip()
        GDGUpDateInfo_NewDate.append(UpDate)

    if (GDGUpDateInfo_NewDate[0] != GDGUpDateInfo_OldDate[0] and os.path.exists('GearDesignGuide.exe') == True):
        os.remove('GearDesignGuide.exe')

    if (GDGUpDateInfo_NewDate[1] != GDGUpDateInfo_OldDate[1] and os.path.exists('GearDesignGuide.dll') == True):
        os.remove('GearDesignGuide.dll')

    if (GDGUpDateInfo_NewDate[2] != GDGUpDateInfo_OldDate[2] and os.path.exists('./Resource/') == True):
        del_files("./Resource/")


# 检查GearDesignGuide.exe与GearDesignGuide.dll时候存在,不存在则下载
for name in Module:
    if (os.path.exists(name) == False):
        print(f"\n[提示]正在准备部署({name})")

        if (DownloadModule(Module[name]+name, name, f"./{name}") == False):
            os.system("pause")
            sys.exit()


# 如果资源文件夹不存在则创建
if (os.path.exists('./Resource') == False):
    os.mkdir('./Resource')

# 检查资源文件时候存在,不存在则下载
for name in Resource:
    if (os.path.exists(f'./Resource/{name}') == False):
        print(f"\n[提示]正在准备部署({name})")

        if (DownloadModule(Resource_URL+name, name, f"./Resource/{name}") == False):
            os.system("pause")
            sys.exit()


# 创建一个text文件(路径,文件内容)
def text_create(path, msg):
    file = open(path, 'w')
    file.write(msg)
    file.close()


if (os.path.exists('./GDGSetUp.ini') == False):
    text_create('./GDGSetUp.ini', 'UpdateCompleted')

os.system("GearDesignGuide.exe")

# Pyinstaller -F -i LOGO1.ico GearDesignGuideUpDate.py
