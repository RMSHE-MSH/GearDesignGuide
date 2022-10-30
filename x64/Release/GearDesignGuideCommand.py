import re
import os
import sys

# GearDesignGuide命令提示符


class CommandPrompt(object):
    InputList = []

    def __init__(self, Input: str):
        self.Input = Input

    def help(self):
        if (self.InputList[0] == "help"):
            print("\nGearDesignGuideCommand Help\n")
            print("Name\n----")
            print("pop / back")

    # 撤销最后一次的操作;
    def pop(self):
        if (self.InputList[0] == "back" or self.InputList[0] == "pop"):
            if (len(self.InputList) == 1):
                print("pop")

            else:
                for i in range(int(self.InputList[1])):
                    print("pop")

    def CommandPrompt(self):
        # 字符串全部转为小写,以空格拆分命令字符串
        self.InputList = self.Input.lower().split()

        # 以命令中参数的多少(包含命令名)对命令进行分类
        if len(self.InputList) == 1:
            self.help()
            self.pop()

        elif len(self.InputList) == 2:
            self.pop()


while 1:
    Input = input(">>")
    if (Input.replace('.', '', 1).isdigit() == False):
        CMP = CommandPrompt(Input)
        CMP.CommandPrompt()
