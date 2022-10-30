"""
    <GearDesignGuideUpDate>
    Copyright (C) <2022>  <RMSHE>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Electronic Mail: asdfghjkl851@outlook.com
"""

import requests
import os
import sys
from time import sleep
from shutil import copy

print("GearDesignGuideUpDate - Powered by RMSHE\n")

Module = {
    "GearDesignGuide.exe": "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/",
    "GearDesignGuide.dll": "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/",
    "GearDesignGuideUpDate.exe": "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/",
}

UpDateInfo_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/GDGUpDateInfo.ini?inline=false"
GDGUpDateInfo_Path = "./GDGUpDateInfo.ini"
GDGUpDateInfo_CachePath = "./Cache/GDGUpDateInfo.ini"

GDGEXE_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/GearDesignGuide.exe"
GDGEXE_CachePath = "./Cache/GearDesignGuide.exe"

GDGDLL_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/GearDesignGuide.dll"
GDGDLL_CachePath = "./Cache/GearDesignGuide.dll"

GDGUpDate_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/GearDesignGuideUpDate.exe"
GDGUpDate_CachePath = "./Cache/GearDesignGuideUpDate.exe"

GDGUpDateInfo_OldDate = [0, 0, 0, 0]
GDGUpDateInfo_NewDate = [0, 0, 0, 0]

Resource_URL = "https://gitlab.com/RMSHE-MSH/GearDesignGuide/-/raw/master/x64/Release/Resource/"
Resource = (
    "P203_10-1.png", "P205_10-2.png", "P207_10-3.png", "P208_10-4.png", "P213_10-6.png", "P216_10-7.png",
    "P216_10-8.png", "P218_10-18.png", "P218_10-19.png", "P219_10-20.png", "P221_10-21.png"
)


# 创建一个text文件(路径,文件内容)
def text_create(path, msg):
    file = open(path, 'w')
    file.write(msg)
    file.close()


# 启动主程序
def SetUpMainProgram():
    if (os.path.exists('./GDGSetUp.ini') == False):
        text_create('./GDGSetUp.ini', 'UpdateCompleted')

    os.system("GearDesignGuide.exe")


# 下载组件
class Downloader(object):
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    def start(self):
        Finish = False
        sleep(2)
        res_length = requests.get(self.url, stream=True)
        total_size = int(res_length.headers['Content-Length'])
        # print(res_length.headers)
        # print(res_length)
        if os.path.exists(self.file_path):
            temp_size = os.path.getsize(self.file_path)
            print(f"[续传]当前断点: {(temp_size/1024):.1f}KB/{(total_size/1024):.1f}KB ({self.file_path})")
        else:
            temp_size = 0
            print(f"[提示]正在下载组件 {self.file_path} ({(total_size/1024):.1f}KB)")

        headers = {'Range': 'bytes=%d-' % temp_size,
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}

        sleep(0.5)
        res_left = requests.get(self.url, stream=True, headers=headers)

        with open(self.file_path, "ab") as f:
            for chunk in res_left.iter_content(chunk_size=1024):
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                done = int(50 * temp_size / total_size)
                sys.stdout.write(
                    f"\r|{'█' * done}{' ' * (50 - done)} | {(temp_size/1024):.1f}KB ({(100 * temp_size / total_size):.1f}%)")
                sys.stdout.flush()

        if os.path.exists(self.file_path):
            if ((100 * temp_size / total_size) >= 100):
                Finish = True

        if (Finish == False):
            print(f"\n[错误]组件下载失败({self.file_path})")

        print("\n")
        return Finish


def DownloadModule(URL: str, file_path: str):
    downloader = Downloader(URL, file_path)
    return downloader.start()


"""
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
"""


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


# 判断网络状态
def NetworkStatus():
    response = os.system("ping gitlab.com -n 1")
    os.system('cls')
    print("GearDesignGuideUpDate - Powered by RMSHE\n")
    return True if response == 0 else False


# 复制安装文件(a -> b)
def CopyInstallFile(a_path, b_path):
    # 如果新版文件存在则执行复制操作(更新)
    if (os.path.exists(a_path) == True):
        # 如果旧版文件存在,则删除旧版文件
        if (os.path.exists(b_path) == True):
            os.remove(b_path)
        # 复制新版文件到运行目录,如果复制完成并且下载缓存目录中的新版文件存在,则删除缓存的新版文件
        if (copy(a_path, b_path) and os.path.exists(a_path)):
            os.remove(a_path)


# 文件不存在型更新(用于首次安装)
def FirstInstall():
    # 检查GearDesignGuide.exe与GearDesignGuide.dll是否存在,不存在则下载
    for name in Module:
        if (os.path.exists(name) == False):
            if (DownloadModule(Module[name]+name, f"./{name}") == False):
                os.system("pause")
                sys.exit()

    # 如果资源文件夹不存在则创建
    if (os.path.exists('./Resource') == False):
        os.mkdir('./Resource')

    # 检查资源文件时候存在,不存在则下载
    for name in Resource:
        if (os.path.exists(f'./Resource/{name}') == False):
            if (DownloadModule(Resource_URL+name, f"./Resource/{name}") == False):
                os.system("pause")
                sys.exit()


# 检查校验各组件是否存在
def ModuleVerify():
    # 检查"GearDesignGuide.exe"与"GearDesignGuide.dll"是否存在,不存在则下载
    for name in Module:
        if (os.path.exists(name) == False):
            if (DownloadModule(Module[name]+name, f"./{name}.Temp") == False):
                os.system("pause")
                sys.exit()
            else:
                os.rename(f"./{name}.Temp", f"./{name}")

    # 如果资源文件夹不存在则创建
    if (os.path.exists('./Resource') == False):
        os.mkdir('./Resource')

    # 检查资源文件时候存在,不存在则下载
    for name in Resource:
        if (os.path.exists(f'./Resource/{name}') == False):
            if (DownloadModule(Resource_URL+name, f"./Resource/{name}.Temp") == False):
                os.system("pause")
                sys.exit()
            else:
                os.rename(f"./Resource/{name}.Temp", f"./Resource/{name}")


# 下载需要更新的文件
def GDGUpdate():
    # GearDesignGuide.exe
    GDGEXE_Finish = True
    if (GDGUpDateInfo_NewDate[0] != GDGUpDateInfo_OldDate[0]):
        GDGEXE_Open = True
        if (DownloadModule(GDGEXE_URL, GDGEXE_CachePath) == True):
            GDGEXE_Finish = True
        else:
            GDGEXE_Finish = False
    else:
        GDGEXE_Open = False

    # GearDesignGuide.dll
    GDGDLL_Finish = True
    if (GDGUpDateInfo_NewDate[1] != GDGUpDateInfo_OldDate[1]):
        GDGDLL_Open = True
        if (DownloadModule(GDGDLL_URL, GDGDLL_CachePath) == True):
            GDGDLL_Finish = True
        else:
            GDGUpDate_Finish = False
    else:
        GDGDLL_Open = False

    # GearDesignGuideUpData.exe
    GDGUpDate_Finish = True
    if (GDGUpDateInfo_NewDate[2] != GDGUpDateInfo_OldDate[2]):
        GDGUpDate_Open = True
        if (DownloadModule(GDGUpDate_URL, GDGUpDate_CachePath) == True):
            GDGUpDate_Finish = True
        else:
            GDGUpDate_Finish = False
    else:
        GDGUpDate_Open = False

    # Resource
    Resource_Finish = True
    if (GDGUpDateInfo_NewDate[3] != GDGUpDateInfo_OldDate[3]):
        Resource_Open = True
        # 逐条下载资源文件
        for name in Resource:
            Resource_Finish = Resource_Finish and DownloadModule(Resource_URL+name, f"./Cache/{name}")
    else:
        Resource_Open = False

    return [[GDGEXE_Open, GDGEXE_Finish], [GDGDLL_Open, GDGDLL_Finish], [GDGUpDate_Open, GDGUpDate_Finish], [Resource_Open, Resource_Finish]]


# 执行部分安装
def InstallUpdate(Install_License):
    # 安装"GearDesignGuide.exe"(主程序)
    if (Install_License[0][0] == True and Install_License[0][1] == True):
        CopyInstallFile(GDGEXE_CachePath, "./GearDesignGuide.exe")

    # 安装"GearDesignGuide.dll"(Math)
    if (Install_License[1][0] == True and Install_License[1][1] == True):
        CopyInstallFile(GDGDLL_CachePath, "./GearDesignGuide.dll")

    # 安装资源文件
    if (Install_License[3][0] == True and Install_License[3][1] == True):
        # 删除旧的资源文件
        if (os.path.exists('./Resource') == True):
            del_files("./Resource/")
        # 复制新的资源文件
        for name in Resource:
            CopyInstallFile(f'./Cache/{name}', f"./Resource/{name}")

    # 告诉"GearDesignGuide.exe",执行"GearDesignGuideUpDate.exe"的安装.
    if (Install_License[2][0] == True and Install_License[2][1] == True):
        if (os.path.exists('./GDGSetUp.ini') == True):
            os.remove('./GDGSetUp.ini')

        if (os.path.exists('./GDGSetUp.ini') == False):
            text_create('./GDGSetUp.ini', 'UpdateCompleted\nInstallUpdate')

            os.startfile(r"GearDesignGuide.exe")
            sys.exit()


if (NetworkStatus() == False):
    print(f"[警告] 无网络连接")
    SetUpMainProgram()
else:
    # 更新UpDateInfo(更新信息),并检查那些组件需要更新
    if (os.path.exists('GDGUpDateInfo.ini') == True):
        # 读取旧的组件版本信息
        listOfLines = Read_ini(GDGUpDateInfo_Path)
        GDGUpDateInfo_OldDate.clear()
        for line in listOfLines:
            OldUpDate = line.strip()
            GDGUpDateInfo_OldDate.append(OldUpDate)

    # 如果资源文件夹不存在则创建
    if (os.path.exists('./Resource') == False):
        os.mkdir('./Resource')
    # 如果下载缓存文件夹不存在则创建
    if (os.path.exists('./Cache') == False):
        os.mkdir('./Cache')
    else:
        # 删除Cache中旧的"GDGUpDateInfo.ini"文件
        if (os.path.exists(GDGUpDateInfo_CachePath) == True):
            os.remove(GDGUpDateInfo_CachePath)

    # 如果GDGUpDateInfo.ini下载成功,则开始检测那些组件需要更新
    if (DownloadModule(UpDateInfo_URL, GDGUpDateInfo_CachePath) == True):
        listOfLines = Read_ini(GDGUpDateInfo_CachePath)

        # 对比新旧组件版本信息
        GDGUpDateInfo_NewDate.clear()
        for line in listOfLines:
            UpDate = line.strip()
            GDGUpDateInfo_NewDate.append(UpDate)

        Install_License = GDGUpdate()  # 下载需要更新的文件

        # 所有需要更新的文件都已被正常下载才会启动安装程序(不包括不需要更新的文件)
        if (Install_License[0][1] == True and Install_License[1][1] == True and Install_License[2][1] == True and Install_License[3][1] == True):
            InstallUpdate(Install_License)

    ModuleVerify()  # 检查校验各组件是否存在,不存在则下载

# 更新"GDGUpDateInfo.ini"文件
CopyInstallFile("./Cache/GDGUpDateInfo.ini", "./GDGUpDateInfo.ini")
SetUpMainProgram()

"""
# 如果组件下载完成,进行安装
if (DownloadModule(GDGEXE_URL, GDGEXE_CachePath) == True):
    # 如果旧版文件存在,则删除旧版文件
    if (os.path.exists("./GearDesignGuide.exe") == True):
        os.remove("./GearDesignGuide.exe")
    # 复制新版文件到运行目录,如果复制完成并且下载缓存目录中的新版文件存在,则删除缓存的新版文件
    if (copy(GDGEXE_CachePath, "./") and os.path.exists(GDGEXE_CachePath)):
        os.remove(GDGEXE_CachePath)
"""

# Pyinstaller -F -i LOGO2.ico GearDesignGuideUpDate.py
