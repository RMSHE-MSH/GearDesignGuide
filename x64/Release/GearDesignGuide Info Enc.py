
import random


str0 = "[AuthorInfo] Powered by RMSHE - asdfghjkl851@outlook.com"
str1 = "[OpenSource] https://github.com/RMSHE-MSH/GearDesignGuide"
str2 = "Copyright (C) RMSHE. All rights reserved."
str3 = "[MathDll] GearDesignGuide.dll - Beta.2022.10.28.Mark0"


def Rand(Length, a, b):
    RandNum = []
    for i in range(Length):
        RandNum.append(random.randint(a, b))
    return RandNum


def toaASCII(Str, RandNum=()):
    ASCII = []
    for i in range(len(Str)):
        ASCII.append(ord(Str[i])-RandNum[i])
    return ASCII


#RandNum = Rand(64, 1, 16)
RandNum = [10, 12, 10, 4, 16, 1, 7, 3, 8, 9, 1, 14, 7, 6, 13, 12, 3, 5, 1, 2, 9, 2, 4, 10, 9, 16, 3, 1, 10, 6, 10,
           4, 9, 12, 14, 9, 10, 1, 3, 11, 12, 7, 13, 16, 11, 13, 7, 7, 3, 9, 5, 11, 2, 9, 16, 11, 2, 4, 7, 3, 12, 3, 14, 14]
print(RandNum)
print(toaASCII(str0, RandNum))
print(toaASCII(str1, RandNum))
print(toaASCII(str2, RandNum))
print(toaASCII(str3, RandNum))
