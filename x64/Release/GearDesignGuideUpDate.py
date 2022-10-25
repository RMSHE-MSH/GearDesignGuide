import requests
import os
import sys
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77'
}


def DownloadBlock(URL: str, file_name: str, file_path: str):
    sleep(1)
    print(f"[下载]正在尝试从({URL})下载{file_name}")
    rf = requests.get(URL, headers)
    if (rf.status_code == 200):
        print(rf, "\n[提示]成功连接服务器,正在下载必要组件...")
    else:
        print(rf, "\n[错误]无法连接服务器")
        return False

    with open(file_path+file_name, "wb") as code:
        code.write(rf.content)
    rf.close()

    if (os.path.exists(file_path+file_name) == False):
        print(f"[致命错误]{file_path+file_name}下载失败.")
        return False
    else:
        print(f"[提示]{file_path+file_name}组件已下载.")
        return True


if (os.path.exists('GearDesignGuide.exe') == False):
    print("[提示]正在启动安装程序...")
    URL_GDG_EXE = "https://tmp-titan.vx-cdn.com/file-6357aafa2a4cb-6357ab9488c76/GearDesignGuide.exe"

    if (DownloadBlock(URL_GDG_EXE, "GearDesignGuide.exe", "") == False):
        os.system("pause")
        sys.exit()
    else:
        os.system("GearDesignGuide.exe")
else:
    os.system("GearDesignGuide.exe")

# Pyinstaller -F -i LOGO1.ico GearDesignGuideUpDate.py
