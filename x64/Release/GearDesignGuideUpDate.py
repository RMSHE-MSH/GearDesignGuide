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

Resource_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/Resource/"
Resource = (
    "P203_10-1.png", "P205_10-2.png", "P207_10-3.png", "P208_10-4.png", "P213_10-6.png", "P216_10-7.png",
    "P216_10-8.png", "P218_10-18.png", "P218_10-19.png", "P219_10-20.png", "P221_10-21.png"
)


def DownloadModule(URL: str, file_name: str, file_path: str):
    sleep(1)
    print(f"[提示]正在尝试访问({URL})")
    rf = requests.get(URL,  headers)
    if (rf.status_code == 200):
        print(f"[提示]正在下载组件({file_name})...")
    else:
        print(f"[错误]无法访问服务器({rf})")
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


for name in Module:
    if (os.path.exists(name) == False):
        print(f"\n[提示]正在准备部署({name})")

        if (DownloadModule(Module[name]+name, name, f"./{name}") == False):
            os.system("pause")
            sys.exit()


if (os.path.exists('./Resource') == False):
    os.mkdir('./Resource')

for name in Resource:
    if (os.path.exists(f'./Resource/{name}') == False):
        print(f"\n[提示]正在准备部署({name})")

        if (DownloadModule(Resource_URL+name, name, f"./Resource/{name}") == False):
            os.system("pause")
            sys.exit()


os.system("GearDesignGuide.exe")

# Pyinstaller -F -i LOGO1.ico GearDesignGuideUpDate.py
