import requests
import os
import sys
from time import sleep

print("GearDesignGuideUpDate - Powered by RMSHE")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77'
}

Module = {
    "GearDesignGuide.exe": "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/",
    "GearDesignGuide.dll": "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/",
}
UpDateInfo_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/GDGUpDateInfo.ini"
Resource_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/Resource/"
Resource = (
    "P203_10-1.png", "P205_10-2.png", "P207_10-3.png", "P208_10-4.png", "P213_10-6.png", "P216_10-7.png",
    "P216_10-8.png", "P218_10-18.png", "P218_10-19.png", "P219_10-20.png", "P221_10-21.png"
)


def DownloadModule(URL: str, file_name: str, file_path: str, Mode: str = "Download"):
    sleep(1)
    if (Mode == "Download"):
        print(f"[提示]正在下载组件({file_name})")

    rf = requests.get(URL,  headers)
    if (rf.status_code != 200):
        print(f"[错误]无法访问服务器({URL} / {rf})")
        return False

    with open(file_path, "wb") as code:
        code.write(rf.content)
    rf.close()

    if (os.path.exists(file_path) == False):
        if (Mode == "Download"):
            print(f"[错误]组件下载失败({file_path})")
        else:
            print(f"[错误]无法下载更新引导({file_path})")
        return False
    else:
        if (Mode == "Download"):
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


# 更新UpDateInfo(更新信息),并检查那些组件需要更新
if (os.path.exists('GDGUpDateInfo.ini') == True):
    os.remove('GDGUpDateInfo.ini')

if (DownloadModule(UpDateInfo_URL, "./GDGUpDateInfo.ini", "UpDate") == True):
    # Open file
    fileHandler = open("GDGUpDateInfo.ini",  "r")
    # Get list of all lines in file
    listOfLines = fileHandler.readlines()
    # Close file
    fileHandler.close()

    # Iterate over the lines
    for line in listOfLines:
        UpDate = line.strip()
        if (UpDate == "UpDate GearDesignGuide.exe"):
            os.remove('GearDesignGuide.exe')
        if (UpDate == "UpDate GearDesignGuide.dll"):
            os.remove('GearDesignGuide.dll')
        if (UpDate == "UpDate Resource"):
            del_files("./Resource/")

if (os.path.exists('GDGUpDateInfo.ini') == True):
    os.remove('GDGUpDateInfo.ini')

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


os.system("GearDesignGuide.exe")

# Pyinstaller -F -i LOGO1.ico GearDesignGuideUpDate.py
