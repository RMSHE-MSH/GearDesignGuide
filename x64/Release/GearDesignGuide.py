# 渐开线圆柱直齿轮副优化设计计算向导
# Powered by RMSHE / 2022.10.18
# Python 3.9.13 64-bit
from ctypes import *
from decimal import *
from math import *
from time import sleep
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
import csv
import re
import requests
import os
import sys

app = QApplication([])
window = QMainWindow()
window.resize(500, 400)
window.move(300, 300)
window.setWindowTitle('GearDesignGuide - Powered by RMSHE')

window.show()
app.exec_()

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
        print(f"[致命错误]{file_path+file_name}不存在, 下载失败.")
        return False
    else:
        print(f"[提示]{file_path+file_name}组件已下载.")
        return True


if (os.path.exists('GearDesignGuide.dll') == False):
    print("[致命错误]GearDesignGuide.dll核心组件不存在.")
    QMessageBox.critical(window, '致命错误', 'GearDesignGuide.dll核心组件不存在.')

    URL_GDG_DLL = "https://gitee.com/rmshe/GearDesignGuide/raw/master/x64/Release/GearDesignGuide.dll"

    if (DownloadBlock(URL_GDG_DLL, "GearDesignGuide.dll", "") == False):
        os.system("pause")
        sys.exit()

URL_IMGDATA = "https://gitee.com/rmshe/GearDesignGuide/raw/master/x64/Release/IMGDATA/"
NAME_IMGDATA = [
    "P203_10-1.png", "P205_10-2.png", "P207_10-3.png", "P208_10-4.png",
    "P213_10-6.png", "P216_10-7.png", "P216_10-8.png", "P218_10-18.png",
    "P218_10-19.png", "P219_10-20.png", "P221_10-21.png"
]
for i in range(11):
    if (os.path.exists(f'./IMGDATA/{NAME_IMGDATA[i]}') == False):
        print(f"\n[错误]{NAME_IMGDATA[i]}资源不存在.")
        if (os.path.exists('./IMGDATA') == False):
            os.mkdir('./IMGDATA')

        if (DownloadBlock(URL_IMGDATA+NAME_IMGDATA[i], NAME_IMGDATA[i], "./IMGDATA/") == False):
            os.system("pause")
            sys.exit()


MathDll = CDLL("./GearDesignGuide.dll")
if (MathDll.Info(114514) != 114514):
    print("[致命错误]GearDesignGuide.dll未响应")
    QMessageBox.critical(window, '致命错误', 'GearDesignGuide.dll未响应.')
    os.system("pause")
    sys.exit()


Point = False  # 所有的数据按向导导引手动查表输入
Bulk = True  # 批量读取"InputData.csv"中的预设数据


class GearData:
    InputPower: float = None  # 输入功率(KW)

    n1: float = None  # 小轮转速(r/min)
    n2: float = None  # 大轮转速(r/min)
    z1_ima: float = None  # 小轮齿数(初选齿数)
    z2_ima: float = None  # 大轮齿数(初选齿数)

    u_ima: float = None  # 理论齿数比(理论传动比)
    u_rel: float = None  # 实际齿数比(实际传动比)
    u_err: float = None  # 实际传动比相对理论传动比的误差

    Lh: int = None  # 工作寿命(h)

    AlphaN: float = 20  # 法截面中的压力角(°)

    Level: int = 7  # 齿轮精度等级

    Material1: str = ""  # 小轮材料与热处理方式
    Material2: str = ""  # 大轮材料与热处理方式
    G1Hardness: str = ""  # 小轮硬度
    G2Hardness: str = ""  # 大轮硬度

    KH_test: float = None  # 试选载荷系数KHt
    T1: float = None  # 小轮转矩T1
    T2: float = None  # 大轮转矩T2

    PHI_d: float = None  # 齿宽系数
    ZH: float = None  # 区域系数
    ZE: float = None  # 弹性影响系数

    Zepsilon: float = None  # 重合度系数

    sigmaHlim1: int = None  # 小轮接触疲劳极限
    sigmaHlim2: int = None  # 大轮接触疲劳极限

    N1: float = None  # 小轮应力循环次数
    N2: float = None  # 大轮应力循环次数

    KHN1: float = None  # 小轮接触疲劳寿命系数
    KHN2: float = None  # 大轮接触疲劳寿命系数

    sigmaH: float = None  # 最小接触疲劳[许用应力]

    d1_test: float = None  # 试算小轮分度圆直径(mm)

    V1_H: float = None  # 小轮圆周速度(m\s)
    b1_H: float = None  # 小轮齿宽(mm)

    KHA: float = None  # 使用系数KHA
    KHV: float = None  # 动载系数KHV

    NULL1: float = None  # (KA/Ft1)/b
    KHAlpha: float = None  # 齿间载荷分配系数KHalpha
    KHbeta: float = None  # 齿向载荷分布系数KHbeta

    KH_rel: float = None  # 实际载荷系数

    d1H_rel: float = None  # 按齿轮表面疲劳强度设计的分度圆直径(mm)
    mH: float = None  # 按齿轮表面疲劳强度设计都的模数(mm)

    KF_test: float = None  # 试选载荷系数KFt

    Y_epsilon: float = None  # 重合度系数Y_epsilon

    YFa1: float = None  # 小轮齿形系数
    YSa1: float = None  # 小轮应力修正系数
    YFa2: float = None  # 大轮齿形系数
    YSa2: float = None  # 大轮应力修正系数

    sigmaFlim1: int = None  # 小轮齿根弯曲疲劳极限
    sigmaFlim2: int = None  # 大轮齿根弯曲疲劳极限
    KFN1: float = None  # 小轮弯曲疲劳寿命系数
    KFN2: float = None  # 大轮弯曲疲劳寿命系数

    SafeF: float = None  # 弯曲疲劳安全系数

    sigmaF: float = None  # 最小接触弯曲[许用应力]

    NULL2: float = None  # 最大(YFa*YSa)/[σF]

    mF_test: float = None  # 试算模数mF_test

    d1F_test: float = None  # 按弯曲疲劳强度设计试算小轮分度圆直径
    VF_test: float = None  # 按弯曲疲劳强度设计试算小轮圆周速度
    bF: float = None  # 按弯曲疲劳强度设计试算的齿宽
    NULL3: float = None  # 宽高比b/h

    KFV: float = None  # 动载系数KFV
    NULL4: float = None  # KA*Ft/b
    KFAlpha: float = None  # 齿间载荷分配系数KFalpha

    KFbeta: float = None  # 齿向载荷分布系数KFbeta
    KF: float = None  # 实际载荷系数KF

    mF: float = None  # 按弯曲疲劳强度设计的模数;
    d1F: float = None  # 按弯曲疲劳强度设计的小轮分度圆直径;

    m_rel = None  # 实际计算模数
    m = None  # 实际圆整模数
    d1_rel = None  # 小轮实际分度圆直径
    d2_rel = None  # 大轮实际分度圆直径
    z1_rel = None  # 小轮实际齿数
    z2_rel = None  # 大轮实际齿数
    a = None  # 实际中心距
    b1 = None  # 小轮实际齿宽
    b2 = None  # 大轮实际齿宽

    check_sigmaH: float = None  # 实际(校核)齿面接触疲劳强度
    F_tangential: float = None  # 两轮实际切向力
    check_sigmaF: float = None  # 实际(校核)齿根接弯曲劳强度

    Axis1_PHI: float = None  # 小齿轮轴径
    Axis2_PHI: float = None  # 大齿轮轴径
    Key1 = None  # 小齿轮键型[键宽键高b*h, 键长L, 毂槽深t1]
    Key2 = None  # 大齿轮键型[键宽键高b*h, 键长L, 毂槽深t1]
    Gear1_OtherGeo = None  # 小轮其余几何参数[全齿高h, 齿顶圆直径da, 齿根圆直径df, 齿厚s]
    Gear2_OtherGeo = None  # 大轮其余几何参数[全齿高h, 齿顶圆直径da, 齿根圆直径df, 齿厚s]
    Gear1StructType = None  # 小轮结构类型
    Gear2StructType = None  # 大轮结构类型
    Gear1Struct = None  # 小轮结构[轮毂宽hub_b, 轮毂直径hub_d, 倒角chamfer, 轮缘内径rim_d, 腹板孔到轴心的直径hole_EQSd, 腹板孔直径hole_d, 腹板厚web_b]
    Gear2Struct = None  # 大轮结构[轮毂宽hub_b, 轮毂直径hub_d, 倒角chamfer, 轮缘内径rim_d, 腹板孔到轴心的直径hole_EQSd, 腹板孔直径hole_d, 腹板厚web_b]


def WriteGearData():
    with open("GearData.csv", "w", newline='') as csvfile:
        GD = csv.writer(csvfile)
        GD.writerow(["输入功率(KW)", "InputPower", GearData.InputPower])
        GD.writerow(["小轮转速(r/min)", "n1", GearData.n1])
        GD.writerow(["大轮转速(r/min)", "n2", GearData.n2])
        GD.writerow(["小轮初选齿数", "z1_ima", GearData.z1_ima])
        GD.writerow(["大轮初选齿数", "z2_ima", GearData.z2_ima])
        GD.writerow(["小轮实际齿数", "z1_rel", GearData.z1_rel])
        GD.writerow(["大轮实际齿数", "z2_rel", GearData.z2_rel])
        GD.writerow(["理论齿数比(理论传动比)", "u_ima", GearData.u_ima])
        GD.writerow(["实际齿数比(实际传动比)", "u_rel", GearData.u_rel])
        GD.writerow(["传动比误差", "u_err", GearData.u_err])
        GD.writerow(["工作寿命(h)", "Lh", GearData.Lh])
        GD.writerow(["法截面中的压力角(°)", "AlphaN", GearData.AlphaN])
        GD.writerow(["齿轮精度等级", "Level", GearData.Level])
        GD.writerow(["小轮材料与热处理方式", "Material1", GearData.Material1])
        GD.writerow(["大轮材料与热处理方式", "Material2", GearData.Material2])
        GD.writerow(["小轮硬度", "G1Hardness", GearData.G1Hardness])
        GD.writerow(["大轮硬度", "G2Hardness", GearData.G2Hardness])
        GD.writerow(["试选载荷系数", "KH_test", GearData.KH_test])
        GD.writerow(["小轮转矩", "T1", GearData.T1])
        GD.writerow(["大轮转矩", "T2", GearData.T2])
        GD.writerow(["齿宽系数", "PHI_d", GearData.PHI_d])
        GD.writerow(["区域系数", "ZH", GearData.ZH])
        GD.writerow(["弹性影响系数", "ZE", GearData.ZE])
        GD.writerow(["重合度系数", "Zepsilon", GearData.Zepsilon])
        GD.writerow(["小轮接触疲劳极限", "sigmaHlim1", GearData.sigmaHlim1])
        GD.writerow(["大轮接触疲劳极限", "sigmaHlim2", GearData.sigmaHlim2])
        GD.writerow(["小轮应力循环次数", "N1", GearData.N1])
        GD.writerow(["大轮应力循环次数", "N2", GearData.N2])
        GD.writerow(["小轮接触疲劳寿命系数", "KHN1", GearData.KHN1])
        GD.writerow(["大轮接触疲劳寿命系数", "KHN2", GearData.KHN2])
        GD.writerow(["最小接触疲劳许用应力", "sigmaH", GearData.sigmaH])
        GD.writerow(["试算小轮分度圆直径", "d1_test", GearData.d1_test])
        GD.writerow(["小轮圆周速度", "V1_H", GearData.V1_H])
        GD.writerow(["小轮齿宽", "b1_H", GearData.b1_H])
        GD.writerow(["使用系数", "KHA", GearData.KHA])
        GD.writerow(["动载系数", "KHV", GearData.KHV])
        GD.writerow(["(KA*Ft1)/b", "(KHA*F1_test)/b1_H", GearData.NULL1])
        GD.writerow(["齿间载荷分配系数", "KHAlpha", GearData.KHAlpha])
        GD.writerow(["齿向载荷分布系数", "KHbeta", GearData.KHbeta])
        GD.writerow(["实际载荷系数", "KH_rel", GearData.KH_rel])
        GD.writerow(["按齿轮表面疲劳强度设计都的分度圆直径", "d1H_rel", GearData.d1H_rel])
        GD.writerow(["按齿轮表面疲劳强度设计都的模数", "mH", GearData.mH])

        GD.writerow(["试选载荷系数", "KF_test", GearData.KF_test])
        GD.writerow(["重合度系数", "Y_epsilon", GearData.Y_epsilon])
        GD.writerow(["小轮齿形系数", "YFa1", GearData.YFa1])
        GD.writerow(["小轮应力修正系数", "YSa1", GearData.YSa1])
        GD.writerow(["大轮齿形系数", "YFa2", GearData.YFa2])
        GD.writerow(["大轮应力修正系数", "YSa2", GearData.YSa2])
        GD.writerow(["小轮齿根弯曲疲劳极限", "sigmaFlim1", GearData.sigmaFlim1])
        GD.writerow(["大轮齿根弯曲疲劳极限", "sigmaFlim2", GearData.sigmaFlim2])
        GD.writerow(["小轮弯曲疲劳寿命系数", "KFN1", GearData.KFN1])
        GD.writerow(["大轮弯曲疲劳寿命系数", "KFN2", GearData.KFN2])
        GD.writerow(["弯曲疲劳安全系数", "SafeF", GearData.SafeF])
        GD.writerow(["最小弯曲疲劳许用应力", "sigmaF", GearData.sigmaF])
        GD.writerow(["最大(YFa*YSa)/[σF]", "(YFa*YSa)/[σF]", GearData.NULL2])
        GD.writerow(["试算模数", "mF_test", GearData.mF_test])
        GD.writerow(["按弯曲疲劳强度设计试算小轮分度圆直径", "d1F_test", GearData.d1F_test])
        GD.writerow(["按弯曲疲劳强度设计试算小轮圆周速度", "VF_test", GearData.VF_test])
        GD.writerow(["按弯曲疲劳强度设计试算的齿宽", "bF", GearData.bF])
        GD.writerow(["宽高比", "b/h", GearData.NULL3])
        GD.writerow(["动载系数", "KFV", GearData.KFV])
        GD.writerow(["KA*Ft/b", "KA*Ft/b", GearData.NULL4])
        GD.writerow(["齿间载荷分配系数", "KFalpha", GearData.KFAlpha])
        GD.writerow(["齿向载荷分布系数", "KFbeta", GearData.KFbeta])
        GD.writerow(["实际载荷系数", "KF", GearData.KF])
        GD.writerow(["按弯曲疲劳强度设计的模数", "mF", GearData.mF])
        GD.writerow(["按弯曲疲劳强度设计的小轮分度圆直径", "d1F", GearData.d1F])

        GD.writerow(["计算模数", "m_rel", GearData.m_rel])
        GD.writerow(["圆整模数", "m", GearData.m])
        GD.writerow(["小轮实际分度圆直径", "d1_rel", GearData.d1_rel])
        GD.writerow(["大轮实际分度圆直径", "d2_rel", GearData.d2_rel])
        GD.writerow(["小轮实际齿数", "z1_rel", GearData.z1_rel])
        GD.writerow(["大轮实际齿数", "z2_rel", GearData.z2_rel])
        GD.writerow(["实际中心距", "a", GearData.a])
        GD.writerow(["小轮实际齿宽", "b1", GearData.b1])
        GD.writerow(["大轮实际齿宽", "b2", GearData.b2])

        GD.writerow(["实际(校核)齿面接触疲劳强度", "check_sigmaH", GearData.check_sigmaH])
        GD.writerow(["两轮实际切向力", "F_tangential", GearData.F_tangential])
        GD.writerow(["实际(校核)齿根接弯曲劳强度", "check_sigmaF", GearData.check_sigmaF])

        GD.writerow(["小齿轮轴径", "Axis1_PHI", GearData.Axis1_PHI])
        GD.writerow(["大齿轮轴径", "Axis2_PHI", GearData.Axis2_PHI])
        GD.writerow(["小齿轮键宽键高键长毂槽深[b,h,l,t1]", "Key1_bhlt1", "["+str(GearData.Key1[0][0])+"," +
                    str(GearData.Key1[0][1])+","+str(GearData.Key1[1])+","+str(GearData.Key1[2])+"]"])
        GD.writerow(["大齿轮键宽键高键长毂槽深[b,h,l,t1]", "Key2_bhlt1", "["+str(GearData.Key2[0][0])+"," +
                    str(GearData.Key2[0][1])+","+str(GearData.Key2[1])+","+str(GearData.Key2[2])+"]"])

        GD.writerow(["小轮全齿高", "Geo_h1", GearData.Gear1_OtherGeo[0]])
        GD.writerow(["小轮齿顶圆直径", "Geo_da1", GearData.Gear1_OtherGeo[1]])
        GD.writerow(["小轮齿根圆直径", "Geo_df1", GearData.Gear1_OtherGeo[2]])
        GD.writerow(["小轮齿厚", "Geo_s1", GearData.Gear1_OtherGeo[3]])

        GD.writerow(["大轮全齿高", "Geo_h2", GearData.Gear2_OtherGeo[0]])
        GD.writerow(["大轮齿顶圆直径", "Geo_da2", GearData.Gear2_OtherGeo[1]])
        GD.writerow(["大轮齿根圆直径", "Geo_df2", GearData.Gear2_OtherGeo[2]])
        GD.writerow(["大轮齿厚", "Geo_s2", GearData.Gear2_OtherGeo[3]])

        GD.writerow(["小轮结构类型", "Gear1StructType", GearData.Gear1StructType])
        GD.writerow(["大轮结构类型", "Gear2StructType", GearData.Gear2StructType])

        if (GearData.Gear1StructType == "实心式"):
            GD.writerow(["小轮轮毂宽", "hub1_b", GearData.Gear1Struct[0]])
            GD.writerow(["小轮轮毂直径", "hub1_d", GearData.Gear1Struct[1]])
            GD.writerow(["小轮倒角", "chamfer1", GearData.Gear1Struct[2]])
        else:
            GD.writerow(["小轮轮毂宽", "hub1_b", GearData.Gear1Struct[0]])
            GD.writerow(["小轮轮毂直径", "hub1_d", GearData.Gear1Struct[1]])
            GD.writerow(["小轮倒角", "chamfer1", GearData.Gear1Struct[2]])
            GD.writerow(["小轮轮缘内径", "rim1_d", GearData.Gear1Struct[3]])
            GD.writerow(["小轮腹板孔到轴心的直径", "hole1_EQSd", GearData.Gear1Struct[4]])
            GD.writerow(["小轮腹板孔直径", "hole1_d", GearData.Gear1Struct[5]])
            GD.writerow(["小轮腹板厚", "web1_b", GearData.Gear1Struct[6]])

        if (GearData.Gear2StructType == "实心式"):
            GD.writerow(["大轮轮毂宽", "hub2_b", GearData.Gear2Struct[0]])
            GD.writerow(["大轮轮毂直径", "hub2_d", GearData.Gear2Struct[1]])
            GD.writerow(["大轮倒角", "chamfer2", GearData.Gear2Struct[2]])
        else:
            GD.writerow(["大轮轮毂宽", "hub2_b", GearData.Gear2Struct[0]])
            GD.writerow(["大轮轮毂直径", "hub2_d", GearData.Gear2Struct[1]])
            GD.writerow(["大轮倒角", "chamfer2", GearData.Gear2Struct[2]])
            GD.writerow(["大轮轮缘内径", "rim2_d", GearData.Gear2Struct[3]])
            GD.writerow(["大轮腹板孔到轴心的直径", "hole2_EQSd", GearData.Gear2Struct[4]])
            GD.writerow(["大轮腹板孔直径", "hole2_d", GearData.Gear2Struct[5]])
            GD.writerow(["大轮腹板厚", "web2_b", GearData.Gear2Struct[6]])


def WriteInputData():
    with open("InputData.csv", "w", newline='') as csvfile:
        ID = csv.writer(csvfile)
        ID.writerow(["输入功率(KW)", "InputPower", GearData.InputPower])
        ID.writerow(["理论齿数比", "u_ima", GearData.u_ima])
        ID.writerow(["小轮转速(r/min)", "n1", GearData.n1])
        ID.writerow(["工作寿命(h)", "Lh", GearData.Lh])
        ID.writerow(["齿轮精度等级", "Level", GearData.Level])
        ID.writerow(["小轮材料与热处理方式", "Material1", GearData.Material1])
        ID.writerow(["大轮材料与热处理方式", "Material2", GearData.Material2])
        ID.writerow(["小轮硬度", "G1Hardness", GearData.G1Hardness])
        ID.writerow(["大轮硬度", "G2Hardness", GearData.G2Hardness])
        ID.writerow(["小轮初选齿数", "z1_ima", GearData.z1_ima])
        ID.writerow(["试选载荷系数", "KH_test", GearData.KH_test])
        ID.writerow(["齿宽系数", "PHI_d", GearData.PHI_d])
        ID.writerow(["弹性影响系数", "ZE", GearData.ZE])
        ID.writerow(["小轮接触疲劳极限", "sigmaHlim1", GearData.sigmaHlim1])
        ID.writerow(["大轮接触疲劳极限", "sigmaHlim2", GearData.sigmaHlim2])
        ID.writerow(["小轮接触疲劳寿命系数", "KHN1", GearData.KHN1])
        ID.writerow(["大轮接触疲劳寿命系数", "KHN2", GearData.KHN2])
        ID.writerow(["使用系数", "KHA", GearData.KHA])
        #ID.writerow(["动载系数", "KHV", GearData.KHV])
        #ID.writerow(["齿间载荷分配系数", "KHAlpha", GearData.KHAlpha])
        ID.writerow(["齿向载荷分布系数", "KHbeta", GearData.KHbeta])
        ID.writerow(["试选载荷系数", "KF_test", GearData.KF_test])
        #ID.writerow(["小轮齿形系数", "YFa1", GearData.YFa1])
        #ID.writerow(["小轮应力修正系数", "YSa1", GearData.YSa1])
        #ID.writerow(["大轮齿形系数", "YFa2", GearData.YFa2])
        #ID.writerow(["大轮应力修正系数", "YSa2", GearData.YSa2])
        ID.writerow(["小轮齿根弯曲疲劳极限", "sigmaFlim1", GearData.sigmaFlim1])
        ID.writerow(["大轮齿根弯曲疲劳极限", "sigmaFlim2", GearData.sigmaFlim2])
        ID.writerow(["小轮弯曲疲劳寿命系数", "KFN1", GearData.KFN1])
        ID.writerow(["大轮弯曲疲劳寿命系数", "KFN2", GearData.KFN2])
        ID.writerow(["弯曲疲劳安全系数", "SafeF", GearData.SafeF])
        #ID.writerow(["动载系数", "KFV", GearData.KFV])
        #ID.writerow(["齿间载荷分配系数", "KFalpha", GearData.KFAlpha])
        #ID.writerow(["齿向载荷分布系数", "KFbeta", GearData.KFbeta])
        #ID.writerow(["圆整模数", "m", GearData.m])
        ID.writerow(["小轮实际齿数", "z1_rel", GearData.z1_rel])
        ID.writerow(["大轮实际齿数", "z2_rel", GearData.z2_rel])
        ID.writerow(["小轮轴径", "Axis1_PHI", GearData.Axis1_PHI])
        ID.writerow(["大轮轴径", "Axis2_PHI", GearData.Axis2_PHI])


def InputBulkData():
    with open('InputData.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in reader:
            if (i[1] == "InputPower"):
                GearData.InputPower = eval(i[2])
            if (i[1] == "u_ima"):
                GearData.u_ima = eval(i[2])
            if (i[1] == "n1"):
                GearData.n1 = eval(i[2])
            if (i[1] == "Lh"):
                GearData.Lh = eval(i[2])
            if (i[1] == "Level"):
                GearData.Level = eval(i[2])
            if (i[1] == "Material1"):
                GearData.Material1 = str(i[2])
            if (i[1] == "Material2"):
                GearData.Material2 = str(i[2])
            if (i[1] == "G1Hardness"):
                GearData.G1Hardness = str(i[2])
            if (i[1] == "G2Hardness"):
                GearData.G2Hardness = str(i[2])
            if (i[1] == "z1_ima"):
                GearData.z1_ima = eval(i[2])
            if (i[1] == "KH_test"):
                GearData.KH_test = eval(i[2])
            if (i[1] == "PHI_d"):
                GearData.PHI_d = eval(i[2])
            if (i[1] == "ZE"):
                GearData.ZE = eval(i[2])
            if (i[1] == "sigmaHlim1"):
                GearData.sigmaHlim1 = eval(i[2])
            if (i[1] == "sigmaHlim2"):
                GearData.sigmaHlim2 = eval(i[2])
            if (i[1] == "KHN1"):
                GearData.KHN1 = eval(i[2])
            if (i[1] == "KHN2"):
                GearData.KHN2 = eval(i[2])
            if (i[1] == "KHA"):
                GearData.KHA = eval(i[2])
            if (i[1] == "KHV"):
                GearData.KHV = eval(i[2])
            if (i[1] == "KHAlpha"):
                GearData.KHAlpha = eval(i[2])
            if (i[1] == "KHbeta"):
                GearData.KHbeta = eval(i[2])
            if (i[1] == "KF_test"):
                GearData.KF_test = eval(i[2])
            if (i[1] == "YFa1"):
                GearData.YFa1 = eval(i[2])
            if (i[1] == "YSa1"):
                GearData.YSa1 = eval(i[2])
            if (i[1] == "YFa2"):
                GearData.YFa2 = eval(i[2])
            if (i[1] == "YSa2"):
                GearData.YSa2 = eval(i[2])
            if (i[1] == "sigmaFlim1"):
                GearData.sigmaFlim1 = eval(i[2])
            if (i[1] == "sigmaFlim2"):
                GearData.sigmaFlim2 = eval(i[2])
            if (i[1] == "KFN1"):
                GearData.KFN1 = eval(i[2])
            if (i[1] == "KFN2"):
                GearData.KFN2 = eval(i[2])
            if (i[1] == "SafeF"):
                GearData.SafeF = eval(i[2])
            if (i[1] == "KFV"):
                GearData.KFV = eval(i[2])
            if (i[1] == "KFalpha"):
                GearData.KFAlpha = eval(i[2])
            if (i[1] == "KFbeta"):
                GearData.KFbeta = eval(i[2])
            if (i[1] == "m"):
                GearData.m = eval(i[2])
            if (i[1] == "z1_rel"):
                GearData.z1_rel = eval(i[2])
            if (i[1] == "z2_rel"):
                GearData.z2_rel = eval(i[2])
            if (i[1] == "Axis1_PHI"):
                GearData.Axis1_PHI = eval(i[2])
            if (i[1] == "Axis2_PHI"):
                GearData.Axis2_PHI = eval(i[2])


def ShowIMGDATA(ImgName):
    MathDll.c_ShowIMGDATA(c_char_p(ImgName.encode("utf-8")))
    """
    path = "./IMGDATA/"+ImgName+".png"
    img = cv.imread(path, 1)
    cv.namedWindow(ImgName)
    cv.imshow(ImgName, img)
    cv.waitKey()
    cv.destroyAllWindows()
    """


# 线性插值(需插值的x坐标,两端基点坐标)将输出x对应的y坐标
def Linear_interpolation(x, x0, y0, x1, y1):
    MathDll.c_Linear_interpolation.restype = c_double
    return MathDll.c_Linear_interpolation(c_double(x), c_double(x0), c_double(y0), c_double(x1), c_double(y1))


# 四舍五入(给定任意浮点数f)
def rounding(f):
    return int(Decimal(str(f)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))


# 当DataMode为True时,程序会略过所有的输入和查表过程,直接批量读取"InputData.csv"中的预设数据进行计算
DataMode = Bulk and os.path.exists('InputData.csv')

if (DataMode == True):
    InputBulkData()


if (DataMode == False or GearData.InputPower == None):
    GearData.InputPower = eval(input("设定输入功率(KW): "))
if (DataMode == False or GearData.u_ima == None):
    GearData.u_ima = eval(input("设定理论齿数比(传动比): "))
if (DataMode == False or GearData.n1 == None):
    GearData.n1 = eval(input("设定小轮转速(r/min): "))

GearData.n2 = GearData.n1 / GearData.u_ima

if (DataMode == False or GearData.Lh == None):
    GearData.Lh = eval(input("工作寿命(h): "))

if (DataMode == False or GearData.Level == None):
    print("\n>[查P216/10-7]确定齿轮精度等级")
    ShowIMGDATA("P216_10-7")
    GearData.Level = eval(input("齿轮精度等级: "))

if (DataMode == False or GearData.Material1 == "" or GearData.Material2 == "" or GearData.G1Hardness == "" or GearData.G2Hardness == ""):
    print("\n>[查P203_10-1]选择两轮材料和热处理方式")
    ShowIMGDATA("P203_10-1")
    if (GearData.G1Hardness == "" or GearData.G2Hardness == ""):
        print("硬度输入必须严格按照此示例格式(\"硬度数值\"+\"硬度单位\"): 286HB / 40HR / 850HV")

    if (GearData.Material1 == ""):
        GearData.Material1 = input("小轮材料与热处理方式: ")
    if (GearData.G1Hardness == ""):
        GearData.G1Hardness = str(input("小轮齿面硬度(HB/HR/HV): "))
    if (GearData.Material2 == ""):
        GearData.Material2 = input("大轮材料与热处理方式: ")
    if (GearData.G2Hardness == ""):
        GearData.G2Hardness = str(input("大轮齿面硬度(HB/HR/HV): "))

if (DataMode == False or GearData.z1_ima == None):
    GearData.z1_ima = eval(input("初选小轮齿数: "))

GearData.z2_ima = GearData.u_ima*GearData.z1_ima

# [按齿轮表面疲劳强度设计]
# 试选载荷系数KH_test
if (DataMode == False or GearData.KH_test == None):
    print("\n>>[按齿轮表面疲劳强度设计]----------------------------------------")
    GearData.KH_test = eval(input("试选载荷系数KHt(一般取1-3): "))
# 小轮转矩T1为
GearData.T1 = 9550000 * GearData.InputPower / GearData.n1
# 大轮转矩T2为
GearData.T2 = 9550000 * GearData.InputPower / GearData.n2
# [查P216/10-8]选择齿宽系数PHId
if (DataMode == False or GearData.PHI_d == None):
    print("\n>[查P216/10-8]选择齿宽系数Φd")
    ShowIMGDATA("P216_10-8")
    GearData.PHI_d = eval(input("齿宽系数Φd: "))
# 区域系数ZH为
GearData.ZH = sqrt(2 / (cos(pi / 180 * GearData.AlphaN) * sin(pi / 180 * GearData.AlphaN)))
# [查P213/10-6]确定弹性影响系数ZE
if (DataMode == False or GearData.ZE == None):
    print("\n>[查P213/10-6]根据齿轮制造方式确定弹性影响系数ZE")
    print(f"小轮材料与热处理方式 = {GearData.Material1}\n大轮材料与热处理方式 = {GearData.Material2}")
    ShowIMGDATA("P213_10-6")
    GearData.ZE = eval(input("弹性影响系数ZE: "))
# 重合度系数Zepsilon为
Alpha_a1 = acos((GearData.z1_ima * cos(pi / 180 * GearData.AlphaN)) / (GearData.z1_ima + 2))
Alpha_a2 = acos((GearData.z2_ima * cos(pi / 180 * GearData.AlphaN)) / (GearData.z2_ima + 2))
epsilonAlpha = (GearData.z1_ima * (tan(Alpha_a1) - tan(pi / 180 * GearData.AlphaN)) +
                GearData.z2_ima * (tan(Alpha_a2) - tan(pi / 180 * GearData.AlphaN))) / (2 * pi)
GearData.Zepsilon = sqrt((4 - epsilonAlpha) / 3)

# 计算接触疲劳许用应力Im_sigmaH
# [查P221/10-21]确定小轮与大轮的接触疲劳极限sigmaHlim(线性插值)
if (DataMode == False or GearData.sigmaHlim1 == None or GearData.sigmaHlim2 == None):
    print("\n>[查P221/10-21]确定小轮与大轮的接触疲劳极限σHlim(注意对应材料和热处理方式)")
    print(f"小轮材料与热处理方式 = {GearData.Material1};\t小轮硬度 = {GearData.G1Hardness};\n大轮材料与热处理方式 = {GearData.Material2};\t大轮硬度 = {GearData.G2Hardness};")
    ShowIMGDATA("P221_10-21")
    if (GearData.sigmaHlim1 == None):
        GearData.sigmaHlim1 = eval(input("小轮接触疲劳极限σHlim1: "))
    if (GearData.sigmaHlim2 == None):
        GearData.sigmaHlim2 = eval(input("大轮接触疲劳极限σHlim2: "))

# 计算应力循环次数N
GearData.N1 = 60 * GearData.n1 * 1 * GearData.Lh
GearData.N2 = 60 * GearData.n2 * 1 * GearData.Lh
# [查P218/10-19]确定接触疲劳寿命系数KHN
if (DataMode == False or GearData.KHN1 == None or GearData.KHN2 == None):
    print("\n>[查P218/10-19]确定接触疲劳寿命系数KHN")
    print(f"小轮应力循环次数: N1 = {GearData.N1:.3E}\n大轮应力循环次数: N2 = {GearData.N2:.3E}")
    ShowIMGDATA("P218_10-19")
    if (GearData.KHN1 == None):
        GearData.KHN1 = eval(input("小轮接触疲劳寿命系数KHN1: "))
    if (GearData.KHN2 == None):
        GearData.KHN2 = eval(input("大轮接触疲劳寿命系数KHN2: "))
# 取安全系数SafeH=1,计算最小接触疲劳许用应力sigmaH
SafeH = 1
sigmaH1 = GearData.KHN1 * GearData.sigmaHlim1 / SafeH
sigmaH2 = GearData.KHN2 * GearData.sigmaHlim2 / SafeH
if (sigmaH1 < sigmaH2):
    GearData.sigmaH = sigmaH1
else:
    GearData.sigmaH = sigmaH2
# 试算小轮分度圆直径d1_test
GearData.d1_test = pow((2 * GearData.KH_test * GearData.T1 / GearData.PHI_d) * ((GearData.u_ima + 1) / GearData.u_ima)
                       * pow(GearData.ZH * GearData.ZE * GearData.Zepsilon / GearData.sigmaH, 2), 1 / 3)
# 计算小轮圆周速度V
GearData.V1_H = (pi * GearData.d1_test * GearData.n1) / (60 * 1000)
# 计算小轮齿宽b1_H
GearData.b1_H = GearData.PHI_d * GearData.d1_test

# 计算实际载荷系数KH
# [查P205/10-2]确定使用系数KHA
if (DataMode == False or GearData.KHA == None):
    print("\n>[查P205/10-2]确定使用系数KHA")
    ShowIMGDATA("P205_10-2")
    GearData.KHA = eval(input("使用系数KHA: "))


# [查P206/10-8]确定动载系数KHV
MathDll.AutoGetKV.restype = c_double
GearData.KHV = MathDll.AutoGetKV(c_int(GearData.Level), c_double(GearData.V1_H))

if (DataMode == False and GearData.KHV == None):
    print("\n>[查P206/10-8]确定动载系数KHV")
    print(f"小轮圆周速度: v = {GearData.V1_H:.3f} m/s;\t齿轮精度等级 = {GearData.Level};")
    ShowIMGDATA("P206_10-8")
    GearData.KHV = eval(input("动载系数KHV: "))


# [查P207/10-3]确定齿间载荷分配系数KHalpha
# 自动查表确定齿间载荷分配系数Kalpha(齿轮硬度, (KA*Ft)/b, 精度等级)
def AutoGet_Kalpha(GHardness, NULL1, Level):
    if (NULL1 >= 100):
        #(KA*Ft)/b >= 100
        if (re.findall('[a-zA-Z]+', GHardness)[0] == "HB" or "hb"):
            # 齿面维式硬度<392为软齿面
            if (Level == 5):
                return 1.0
            elif (Level == 6):
                return 1.0
            elif (Level == 7):
                return 1.0
            elif (Level == 8):
                return 1.1
            else:
                print("[警告]./Kalpha/P207/10-3/(KA*Ft)/b>=100/软齿面{GHardness}/不存在的精度等级 (异常处理: 请手动处理)")
                return None
        else:
            # 齿面维式硬度>=392为硬齿面
            if (Level == 5):
                return 1.0
            elif (Level == 6):
                return 1.0
            elif (Level == 7):
                return 1.1
            elif (Level == 8):
                return 1.2
            else:
                print("[警告]./Kalpha/P207/10-3/(KA*Ft)/b>=100/硬齿面{GHardness}/不存在的精度等级 (异常处理: 请手动处理)")
                return None
    else:
        #(KA*Ft)/b < 100
        if (re.findall('[a-zA-Z]+', GHardness)[0] == "HB" or "hb"):
            # 齿面维式硬度<392为软齿面
            if (Level <= 5):
                return 1.2
            else:
                print(f"[警告]./Kalpha/P207/10-3/(KA*Ft)/b<100/软齿面{GHardness}/精度等级最高应为5,但实际为{Level} (异常处理: 取 Kalpha = 1.2)")
                return 1.2
        else:
            # 齿面维式硬度>=392为硬齿面
            if (Level <= 5):
                return 1.2
            else:
                print(f"[警告]./Kalpha/P207/10-3/(KA*Ft)/b<100/硬齿面{GHardness}/精度等级最高应为5,但实际为{Level} (异常处理: 取 Kalpha = 1.2)")
                return 1.2


F1_test = (2 * GearData.T1) / GearData.d1_test
GearData.NULL1 = ((GearData.KHA * F1_test) / GearData.b1_H)  # (KA*Ft)/b
GearData.KHAlpha = AutoGet_Kalpha(GearData.G1Hardness, GearData.NULL1, GearData.Level)

if (DataMode == False and GearData.KHAlpha == None):
    print("\n>[查P207/10-3]确定齿间载荷分配系数KHalpha")
    if (GearData.NULL1 >= 100):
        print(f"(KA*Ft)/b = {GearData.NULL1:.1f} >= 100 N/mm")
    else:
        print(f"(KA*Ft)/b = {GearData.NULL1:.1f} < 100 N/mm")
    ShowIMGDATA("P207_10-3")
    GearData.KHAlpha = eval(input("齿间载荷分配系数KHalpha: "))

# [查P208/10-4]确定齿向载荷分布系数KHbeta(线性插值)
if (DataMode == False or GearData.KHbeta == None):
    print("\n>[查P208/10-4]齿向载荷分布系数KHbeta(线性插值)")
    print(f"齿宽系数: Φd = {GearData.PHI_d};\t小轮齿宽: b = {GearData.b1_H:.3f} mm;\t齿轮精度等级 = {GearData.Level};")
    ShowIMGDATA("P208_10-4")
    GearData.KHbeta = eval(input("齿向载荷分布系数KHbeta: "))
# 实际载荷系数KH_rel为
GearData.KH_rel = GearData.KHA * GearData.KHV * GearData.KHAlpha * GearData.KHbeta

# 使用实际载荷系数计算分度圆直径d1H_rel, 以及相应的模数mH
GearData.d1H_rel = GearData.d1_test * pow((GearData.KH_rel / GearData.KH_test), 1 / 3)
GearData.mH = GearData.d1H_rel / GearData.z1_ima

# [按齿根弯曲疲劳强度设计]
# 试选载荷系数KF_test
if (DataMode == False or GearData.KF_test == None):
    print("\n>>[按齿根弯曲疲劳强度设计]----------------------------------------")
    GearData.KF_test = eval(input("试选载荷系数KFt(一般与KHt相同): "))
# 计算重合度系数Y_epsilon
GearData.Y_epsilon = 0.25 + (0.75 / epsilonAlpha)

# 计算(YFa*YSa)/[σF]


# [查P211/10-5]确定齿形系数Y_Fa1, Y_Fa2; 应力修正系数Y_Sa1, Y_Sa2;(线性插值)
def AutoGet_YFa_YSa(z):
    # 需给定齿数
    z_s = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 150, 200]
    YFa_s = [2.97, 2.91, 2.85, 2.80, 2.76, 2.72, 2.69, 2.65, 2.62, 2.60, 2.57, 2.55, 2.53,
             2.52, 2.45, 2.40, 2.35, 2.32, 2.28, 2.24, 2.22, 2.20, 2.18, 2.14, 2.12, 2.06]
    YSa_s = [1.52, 1.53, 1.54, 1.55, 1.56, 1.57, 1.575, 1.58, 1.59, 1.595, 1.60, 1.61,
             1.62, 1.625, 1.65, 1.67, 1.68, 1.70, 1.73, 1.75, 1.77, 1.78, 1.79, 1.83, 1.865, 1.97]

    if (z > 200):
        return [2.06, 1.97]

    for i in range(len(z_s)):
        if (z == z_s[i]):
            return [YFa_s[i], YSa_s[i]]
        else:
            if (z_s[i-1] < z < z_s[i]):
                # 线性插值
                YFa = Linear_interpolation(z, z_s[i-1], YFa_s[i-1], z_s[i], YFa_s[i])
                YSa = Linear_interpolation(z, z_s[i-1], YSa_s[i-1], z_s[i], YSa_s[i])
                return [YFa, YSa]


_YFS1 = AutoGet_YFa_YSa(GearData.z1_ima)
GearData.YFa1 = _YFS1[0]
GearData.YSa1 = _YFS1[1]

_YFS2 = AutoGet_YFa_YSa(rounding(GearData.z2_ima))
GearData.YFa2 = _YFS2[0]
GearData.YSa2 = _YFS2[1]

"""
if (DataMode == False or GearData.YFa1 == None or GearData.YSa1 == None or GearData.YFa2 == None or GearData.YSa2 == None):
    print("\n>[查P211/10-5确定齿形系数Y_Fa1, Y_Fa2; 应力修正系数Y_Sa1, Y_Sa2; (线性插值)")
    print(f"小轮齿数: z1 = {GearData.z1_ima};\t大轮齿数: z2 = {Decimal(str(GearData.z2_ima)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)};")
    ShowIMGDATA("P211_10-5")
    if (GearData.YFa1 == None):
        GearData.YFa1 = eval(input("小轮齿形系数YFa1: "))
    if (GearData.YSa1 == None):
        GearData.YSa1 = eval(input("小轮应力修正系数YSa1: "))
    if (GearData.YFa2 == None):
        GearData.YFa2 = eval(input("大轮齿形系数YFa2: "))
    if (GearData.YSa2 == None):
        GearData.YSa2 = eval(input("大轮应力修正系数YSa2: "))
"""

# [查P219/10-20]确定小轮和大轮齿根弯曲疲劳极限sigmaFlim1, sigmaFlim2
if (DataMode == False or GearData.sigmaFlim1 == None or GearData.sigmaFlim2 == None):
    print("\n>[查P219/10-20]确定小轮和大轮齿根弯曲疲劳极限σFlim1, σFlim2")
    print(f"小轮材料与热处理方式 = {GearData.Material1};\t小轮硬度 = {GearData.G1Hardness};\n大轮材料与热处理方式 = {GearData.Material2};\t大轮硬度 = {GearData.G2Hardness};")
    ShowIMGDATA("P219_10-20")
    if (GearData.sigmaFlim1 == None):
        GearData.sigmaFlim1 = eval(input("小轮齿根弯曲疲劳极限σFlim1(MPa): "))  # (MPa)
    if (GearData.sigmaFlim2 == None):
        GearData.sigmaFlim2 = eval(input("大轮齿根弯曲疲劳极限σFlim2(MPa): "))  # (MPa)

# [查P218/10-18]确定弯曲疲劳寿命系数KFN
if (DataMode == False or GearData.KFN1 == None or GearData.KFN2 == None):
    print("\n>[查P218/10-18]确定两轮弯曲疲劳寿命系数KFN")
    print(f"小轮应力循环次数: N1 = {GearData.N1:.3E}\n大轮应力循环次数: N2 = {GearData.N2:.3E}")
    ShowIMGDATA("P218_10-18")
    if (GearData.KFN1 == None):
        GearData.KFN1 = eval(input("小轮弯曲疲劳寿命系数KFN1: "))
    if (GearData.KFN2 == None):
        GearData.KFN2 = eval(input("大轮弯曲疲劳寿命系数KFN2: "))

# 取弯曲疲劳安全系数S=1.4, 计算弯曲疲劳许用应力
if (DataMode == False or GearData.SafeF == None):
    GearData.SafeF = eval(input("给定弯曲疲劳安全系数SF(一般取1.25~1.5): "))

Im_sigmaF1 = (GearData.KFN1 * GearData.sigmaFlim1) / GearData.SafeF
Im_sigmaF2 = (GearData.KFN2 * GearData.sigmaFlim2) / GearData.SafeF

# 选择最小的弯曲疲劳强度
if (Im_sigmaF1 < Im_sigmaF2):
    GearData.sigmaF = Im_sigmaF1
else:
    GearData.sigmaF = Im_sigmaF2
# 计算最大(YFa*YSa)/[σF]
NULL2_0 = (GearData.YFa1 * GearData.YSa1) / Im_sigmaF1
NULL2_1 = (GearData.YFa2 * GearData.YSa2) / Im_sigmaF2
if (NULL2_0 > NULL2_1):
    GearData.NULL2 = NULL2_0
else:
    GearData.NULL2 = NULL2_1

# 试算模数mF_test
GearData.mF_test = pow(((2 * GearData.KF_test * GearData.T1 * GearData.Y_epsilon) /
                       (GearData.PHI_d * GearData.z1_ima * GearData.z1_ima)) * GearData.NULL2, 1 / 3)
# 试算小轮圆周速度VF_test
GearData.d1F_test = GearData.mF_test * GearData.z1_ima
GearData.VF_test = (pi * GearData.d1F_test * GearData.n1) / (60 * 1000)
# 计算齿宽bF
GearData.bF = GearData.PHI_d * GearData.d1F_test
# 计算宽高比b/h
hax = 1  # ha*
cx = 0.25  # c*
hF = (2 * hax + cx) * GearData.mF_test
GearData.NULL3 = GearData.bF / hF  # b/h

# [查P206/10-8]确定动载系数KFV
GearData.KFV = MathDll.AutoGetKV(c_int(GearData.Level), c_double(GearData.VF_test))

if (DataMode == False and GearData.KFV == None):
    print("\n>[查P206/10-8]确定动载系数KFV")
    print(f"小轮圆周速度: v = {GearData.VF_test:.3f} m/s;\t齿轮精度等级 = {GearData.Level};")
    ShowIMGDATA("P206_10-8")
    GearData.KFV = eval(input("动载系数KFV: "))

# [查P207/10-3]确定齿间载荷分配系数KFalpha
KFA = GearData.KHA
F1_test2 = (2 * GearData.T1) / GearData.d1F_test
GearData.NULL4 = (KFA * F1_test2) / GearData.bF
GearData.KFAlpha = AutoGet_Kalpha(GearData.G2Hardness, GearData.NULL4, GearData.Level)

if (DataMode == False and GearData.KFAlpha == None):
    print("\n>[查P207/10-3]确定齿间载荷分配系数KFalpha")
    if (GearData.NULL4 < 100):
        print(f"KA*Ft/b = {GearData.NULL4:.1f} < 100")
    else:
        print(f"KA*Ft/b = {GearData.NULL4:.1f} >= 100")

    ShowIMGDATA("P207_10-3")
    GearData.KFAlpha = eval(input("齿间载荷分配系数KFalpha: "))

# [查P208/10-13]确定弯曲强度计算的齿向载荷分布系数KFbeta
MathDll.AutoGetKFbeta.restype = c_double
GearData.KFbeta = MathDll.AutoGetKFbeta(c_double(GearData.KHbeta), c_double(GearData.bF), c_double(hF))

if (DataMode == False and GearData.KFbeta == None):
    print("\n>[查P208/10-13]确定弯曲强度计算的齿向载荷分布系数KFbeta")
    print(f"齿向载荷分布系数: KHbeta = {GearData.KHbeta:.3f};\tb/h = {GearData.NULL3:.3f};")
    ShowIMGDATA("P208_10-13")
    GearData.KFbeta = eval(input("齿向载荷分布系数KFbeta: "))

# 计算实际载荷系数KF
GearData.KF = KFA * GearData.KFV * GearData.KFAlpha * GearData.KFbeta

# 计算齿轮模数mF,以及相应的分度圆直径d1F
GearData.mF = GearData.mF_test * pow((GearData.KF / GearData.KF_test), 1 / 3)
GearData.d1F = GearData.mF * GearData.z1_ima

# [对比计算结果]----------------------------------------
GearData.m_rel = GearData.mF
GearData.d1_rel = GearData.d1H_rel

# [计算几何尺寸]

# 自动圆整模数
m_series1 = [0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 25, 32, 40, 50]
MathDll.GetNearestElement.restype = c_double
GearData.m = MathDll.GetNearestElement((c_double*28)(*m_series1), c_double(GearData.m_rel), c_int(28))

print("\n>>[计算几何尺寸]----------------------------------------")
if (DataMode == False and GearData.m == None):
    print(f"请根据渐开线圆柱齿轮模数系列就近圆整计算模数;\t当前计算模数 = {GearData.m_rel:.3f};")
    ShowIMGDATA("GB_T_1357_1987")
    GearData.m = eval(input("圆整模数m: "))

GearData.z1_rel = (GearData.d1_rel / GearData.m)
GearData.z2_rel = (GearData.u_ima * (GearData.d1_rel / GearData.m))

# 判断两轮齿数是否互质


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def coprime(a, b):
    return gcd(a, b) == 1


# 计算齿数四舍五入
GearData.z1_rel = int(Decimal(str(GearData.z1_rel)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
GearData.z2_rel = int(Decimal(str(GearData.z2_rel)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
# 如果齿数不互质则重新手动指定两轮齿数
if (coprime(GearData.z1_rel, GearData.z2_rel) == False):
    print(f"小轮齿数: z1 = {GearData.z1_rel};\t大轮齿数: z2 = {GearData.z2_rel};\n[提示] 两齿轮齿数没有互质!请调整(如不调整则输入原值): ")
    GearData.z1_rel = eval(input("新的小轮齿数z1: "))
    GearData.z2_rel = eval(input("新的大轮齿数z2: "))

# 计算分度圆直径
GearData.d1_rel = GearData.z1_rel*GearData.m
GearData.d2_rel = GearData.z2_rel*GearData.m

# 计算中心距
GearData.a = (GearData.d1_rel+GearData.d2_rel)/2

# 计算齿宽
GearData.b2 = GearData.PHI_d*GearData.d1_rel
GearData.b1 = GearData.b2+5

print("\n>>[轮齿校核]----------------------------------------")
# 动载系数KV不可靠警告
if (not (1.25 <= GearData.m <= 50)):
    print(f"[警告]./动载系数KV/齿轮模数 (m = {GearData.m} mm 不在[1.25,50]区间内) 这将导致动载系数KV不可靠.")
if (not (6 <= GearData.z1_rel <= 1200)):
    print(f"[警告]./动载系数KV/小轮齿数 (z1 = {GearData.z1_rel} 不在[6,1200]区间内) 这将导致动载系数KV不可靠.")
if (not (6 <= GearData.z2_rel <= 1200)):
    print(f"[警告]./动载系数KV/小轮齿数 (z1 = {GearData.z2_rel} 不在[6,1200]区间内) 这将导致动载系数KV不可靠.")

# 计算传动比误差
GearData.u_rel = GearData.z2_rel/GearData.z1_rel
GearData.u_err = (1-(GearData.u_rel/GearData.u_ima))*100
print(f"传动比误差: u_error = {GearData.u_err:.2f} %")

# 校核齿面接触疲劳强度
GearData.check_sigmaH = sqrt(((2*GearData.KH_rel*GearData.T1)/(GearData.PHI_d*pow(GearData.d1_rel, 3))) *
                             ((GearData.u_rel+1)/GearData.u_rel))*GearData.ZH*GearData.ZE*GearData.Zepsilon
if (GearData.check_sigmaH <= GearData.sigmaH):
    # print(f"接触疲劳强度校核通过: σH = {GearData.check_sigmaH:.3f} <= [σH] = {GearData.sigmaH:.3f}")
    pass
else:
    print(f"[警告] 接触疲劳强度校核未通过: σH = {GearData.check_sigmaH:.3f} > [σH] = {GearData.sigmaH:.3f}")

# 校核齿根弯曲触疲劳强度
GearData.F_tangential = (2 * GearData.T1) / GearData.d1_rel  # 两轮切向力大小相同

check_sigmaF1 = (GearData.KF*GearData.F_tangential*GearData.YFa1*GearData.YSa1*GearData.Y_epsilon)/(GearData.b1*GearData.m)
check_sigmaF2 = (GearData.KF*GearData.F_tangential*GearData.YFa2*GearData.YSa2*GearData.Y_epsilon)/(GearData.b2*GearData.m)
if (check_sigmaF1 < check_sigmaF2):
    GearData.check_sigmaF = check_sigmaF1
else:
    GearData.check_sigmaF = check_sigmaF2

if (GearData.check_sigmaF <= GearData.sigmaF):
    # print(f"弯曲疲劳强度校核通过: σF = {GearData.check_sigmaF:.3f} <= [σF] = {GearData.sigmaF:.3f}")
    pass
else:
    print(f"[警告] 弯曲疲劳强度校核未通过: σF = {GearData.check_sigmaF:.3f} > [σF] = {GearData.sigmaF:.3f}")

# 计算两轮结构


# 选择最合适的普通平键(齿轮宽,轴径)
def Key_Select(b, Axis_PHI):
    Axis = [[6, 8], [8, 10], [10, 12], [12, 17], [17, 22], [22, 30], [30, 38], [38, 44], [
        44, 50], [50, 58], [58, 65], [65, 75], [75, 85], [85, 95], [95, 110], [110, 130]]

    Key = [[[2, 2], [6, 20]], [[3, 3], [6, 36]], [[4, 4], [8, 45]], [[5, 5], [10, 56]], [[6, 6], [14, 70]], [[8, 7], [18, 90]], [[10, 8], [22, 110]], [[12, 8], [28, 140]], [
        [14, 9], [36, 160]], [[16, 10], [45, 180]], [[18, 11], [50, 200]], [[20, 12], [56, 220]], [[22, 14], [63, 250]], [[25, 14], [70, 280]], [[28, 16], [80, 320]], [[32, 18], [90, 360]]]

    Length_Series = [6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56,
                     63, 70, 80, 90, 100, 110, 125, 140, 160, 180, 200, 220, 250, 280, 320, 360]

    t1_Series = [1, 1.4, 1.8, 2.3, 2.8, 3.3, 3.3, 3.3, 3.8, 4.3, 4.4, 4.9, 5.4, 5.4, 6.4, 7.4]

    j = 0
    for i in Axis:
        if (i[0] < Axis_PHI <= i[1]):
            Key_bh = Key[j]
            t1 = t1_Series[j]
            break
        j += 1

    for i in Length_Series:
        if (i < b and Key_bh[1][0] <= i <= Key_bh[1][1]):
            Key_l = i

    Key_bhl = [[Key_bh[0][0], Key_bh[0][1]], Key_l, t1]

    return Key_bhl


# 计算齿轮其余的几何尺寸(齿数, 模数)
def GearOtherGeo(z, m):
    # 齿顶高
    ha = m
    # 齿根高
    hf = 1.25*m
    # 全齿高
    h = ha+hf
    # 齿顶圆直径
    da = (z+2)*m
    # 齿根圆直径
    df = (z-2.5)*m
    # 齿厚
    s = z*m*sin((pi/180*90 / z))

    return [h, da, df, s]


# 确定齿轮结构类型(齿顶圆直径, 模数, 键槽到齿根的最小距离)
def GearStructType(da, m, Gear_e):
    if (Gear_e < 2*m):
        # print("[齿轮轴] 小轮与轴一体制造")
        StructType = "齿轮轴"
    else:
        # print("[齿轮] 小轮与轴分开制造")
        if (da <= 160):
            StructType = "实心式"
        elif (160 < da <= 500):
            StructType = "腹板式"
        elif (500 < da < 1000):
            StructType = "轮辐式"
        else:
            StructType = "[错误]齿轮过大"

        return StructType


# 计算齿轮结构(齿轮结构类型, 齿轮宽, 模数, 齿顶圆直径, 轴径)
def GearStruct(_GearStructType, b, m, da, Axis_PHI):
    # 计算轮毂宽
    if (b < 1.5*Axis_PHI):
        hub_b = b
    else:
        hub_b = 2*Axis_PHI

    # 计算轮毂直径(材料为钢)
    hub_d = 1.6*Axis_PHI

    # 计算倒角
    chamfer = 0.5*m

    if (_GearStructType == "实心式"):
        return [hub_b, hub_d, chamfer]
    elif (_GearStructType == "腹板式"):
        # 计算轮缘内径
        rim_d = da-12*m
        # 计算腹板孔到轴心的直径
        hole_EQSd = 0.5*(rim_d+hub_d)
        # 计算腹板孔直径
        hole_d = 0.3*(rim_d-hub_d)
        # 计算腹板厚
        web_b = 0.3*b
        return [hub_b, hub_d, chamfer, rim_d, hole_EQSd, hole_d, web_b]
    elif (_GearStructType == "轮辐式"):
        print("[警告]轮辐式齿轮机构设计我懒得做了(反正课程设计几乎不可能会用到)")
    else:
        print("[错误]齿轮过大")


# 小轮结构设计
if (DataMode == False or GearData.Axis1_PHI == None):
    print("\n>>[小轮结构设计]----------------------------------------")
    print(f"小轮分度圆直径: d1 = {GearData.d1_rel} mm")
    GearData.Axis1_PHI = eval(input("请给定小轮轴直径(mm): "))
GearData.Key1 = Key_Select(GearData.b1, GearData.Axis1_PHI)

# 判断齿轮与轴是否要分开制造
GearData.Gear1_OtherGeo = GearOtherGeo(GearData.z1_rel, GearData.m)
# 计算键槽到齿根的最小距离
Gear1_e = (0.5*GearData.Gear1_OtherGeo[2])-(0.5*GearData.Axis1_PHI+GearData.Key1[2])
# 确定小轮结构类型
GearData.Gear1StructType = GearStructType(GearData.Gear1_OtherGeo[1], GearData.m, Gear1_e)
# 计算齿轮结构
GearData.Gear1Struct = GearStruct(GearData.Gear1StructType, GearData.b1, GearData.m, GearData.Gear1_OtherGeo[1], GearData.Axis1_PHI)

# 大轮结构设计
if (DataMode == False or GearData.Axis2_PHI == None):
    print("\n>>[大轮结构设计]----------------------------------------")
    print(f"大轮分度圆直径: d2 = {GearData.d2_rel} mm")
    GearData.Axis2_PHI = eval(input("请给定大轮轴直径(mm): "))
GearData.Key2 = Key_Select(GearData.b2, GearData.Axis2_PHI)

# 判断齿轮与轴是否要分开制造
GearData.Gear2_OtherGeo = GearOtherGeo(GearData.z2_rel, GearData.m)
# 计算键槽到齿根的最小距离
Gear2_e = (0.5*GearData.Gear2_OtherGeo[2])-(0.5*GearData.Axis2_PHI+GearData.Key2[2])
# 确定小轮结构类型
GearData.Gear2StructType = GearStructType(GearData.Gear2_OtherGeo[1], GearData.m, Gear2_e)
# 计算齿轮结构
GearData.Gear2Struct = GearStruct(GearData.Gear2StructType, GearData.b2, GearData.m, GearData.Gear2_OtherGeo[1], GearData.Axis2_PHI)

WriteInputData()
WriteGearData()

print("\n>>[圆柱直齿轮副设计完成]")

# 生成设计报告
ReportMode = input("\n请选择呈现不同形式的报告:\t[E]设计简报;\t[D]设计参数;\t[R]设计报告;\t[C]设计过程    >>")

if (ReportMode == "E" or ReportMode == "e"):
    print("\n\n--------------------[设计简报]--------------------")
    print(">>[轮齿设计结论]")
    print(f"模数:\tm = {GearData.m} mm;")
    print(f"齿数:\tz1 = {GearData.z1_rel};\tz2 = {GearData.z2_rel};")
    print(f"压力角:\tα = {GearData.AlphaN} °;")
    print(f"全齿高:\th1 = {GearData.Gear1_OtherGeo[0]:.3f} mm;\th2 = {GearData.Gear2_OtherGeo[0]:.3f} mm;")
    print(f"齿厚:\ts1 = {GearData.Gear1_OtherGeo[3]:.3f} mm;\ts2 = {GearData.Gear2_OtherGeo[3]:.3f} mm;")
    print(f"中心距:\ta = {GearData.a} mm;")
    print(f"\n齿宽:\tb1 = {GearData.b1} mm;\tb2 = {GearData.b2} mm;")
    print(f"齿顶圆直径:\tda1 = {GearData.Gear1_OtherGeo[1]:.3f} mm;\tda2 = {GearData.Gear2_OtherGeo[1]:.3f} mm;")
    print(f"齿根圆直径:\tdf1 = {GearData.Gear1_OtherGeo[2]:.3f} mm;\tdf2 = {GearData.Gear2_OtherGeo[2]:.3f} mm;")
    print(f"材料:\t小轮 = {GearData.Material1};\t大轮 = {GearData.Material2};")
    print(f"精度等级:\tLevel = {GearData.Level};")

    print("\n>>[结构设计结论]")
    #print(f"轮结构类型:\t小轮 = {GearData.Gear1StructType};\t大轮 = {GearData.Gear2StructType};")
    #print(f"轴孔径:\t小轮 = {GearData.Axis1_PHI} mm;\t大轮 = {GearData.Axis2_PHI} mm;")

    Key1 = "["+str(GearData.Key1[0][0])+"," + str(GearData.Key1[0][1])+","+str(GearData.Key1[1])+","+str(GearData.Key1[2])+"]"
    Key2 = "["+str(GearData.Key2[0][0])+"," + str(GearData.Key2[0][1])+","+str(GearData.Key2[1])+","+str(GearData.Key2[2])+"]"
    #print(f"键连接[b,h,l,t1]:\t小轮 = {Key1};\t大轮 = {Key2};")

    print("\n>小齿轮结构参考值:")
    print(f"轮结构类型 = {GearData.Gear1StructType};")
    print(f"轴孔径:\tD4 = {GearData.Axis1_PHI} mm;")
    print(f"键连接:\t[b,h,l,t1] = {Key1};")
    if (GearData.Gear1StructType == "实心式"):
        print(f"轮毂宽:\tB = {GearData.Gear1Struct[0]} mm;")
        print(f"轮毂直径:\tD3 = {GearData.Gear1Struct[1]} mm;")
        print(f"倒角:\tn1 = {GearData.Gear1Struct[2]} mm;")
    else:
        print(f"轮毂宽:\tB = {GearData.Gear1Struct[0]} mm;")
        print(f"轮毂直径:\tD3 = {GearData.Gear1Struct[1]} mm;")
        print(f"倒角:\tn1 = {GearData.Gear1Struct[2]} mm;")
        print(f"轮缘内径:\tD0 = {GearData.Gear1Struct[3]} mm;")
        print(f"腹板孔到轴心的直径:\tD1 = {GearData.Gear1Struct[4]} mm;")
        print(f"腹板孔直径:\tD2 = {GearData.Gear1Struct[5]} mm;")
        print(f"腹板厚:\tC = {GearData.Gear1Struct[6]} mm;")

    print("\n>大齿轮结构参考值:")
    print(f"轮结构类型 = {GearData.Gear2StructType};")
    print(f"轴孔径:\tD4 = {GearData.Axis2_PHI} mm;")
    print(f"键连接:\t[b,h,l,t1] = {Key2};")
    if (GearData.Gear2StructType == "实心式"):
        print(f"轮毂宽:\tB = {GearData.Gear2Struct[0]} mm;")
        print(f"轮毂直径:\tD3 = {GearData.Gear2Struct[1]} mm;")
        print(f"倒角:\tn1 = {GearData.Gear2Struct[2]} mm;")
    else:
        print(f"轮毂宽:\tB = {GearData.Gear2Struct[0]} mm;")
        print(f"轮毂直径:\tD3 = {GearData.Gear2Struct[1]} mm;")
        print(f"倒角:\tn1 = {GearData.Gear2Struct[2]} mm;")
        print(f"轮缘内径:\tD0 = {GearData.Gear2Struct[3]} mm;")
        print(f"腹板孔到轴心的直径:\tD1 = {GearData.Gear2Struct[4]} mm;")
        print(f"腹板孔直径:\tD2 = {GearData.Gear2Struct[5]} mm;")
        print(f"腹板厚:\tC = {GearData.Gear2Struct[6]} mm;")

        print("--------------------[简报结束]--------------------")
elif (ReportMode == "D" or ReportMode == "d"):
    print("\n\n--------------------[设计参数]--------------------")
    with open('GearData.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i in reader:
            print(i)
    print("--------------------[参数结束]--------------------")


os.system("pause")

# Pyinstaller -F -i LOGO1.ico GearDesignGuide.py