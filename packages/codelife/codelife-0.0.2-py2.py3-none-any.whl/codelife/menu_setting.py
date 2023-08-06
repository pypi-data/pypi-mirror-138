#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/12 11:12 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : menu_setting.py
# @Project : codelife
import platform
import sys

import renxianqi.shortcut as sc
from codelife import setting

import tkinter.messagebox as mb

from codelife.pip_trigger import upgrade

POPUP_TITLE = "[CodeLife-开发工具]"

def show_copyright():
    message = """
工具采用Apache License，请放心免费使用！
版本：%s
开发者：雷学委
作者网站：https://blog.csdn.net/geeklevin
社区信息：https://py4ever.gitee.io/
欢迎关注公众号【雷学委】，加入Python开发者阵营！
    """ % (setting.VERSION)
    mb.showinfo(POPUP_TITLE, message)



def make_shortcut():
    os_name = platform.system()
    if os_name == "Windows" or "Win" in os_name:
        binpath = sys.argv[0]
        if not binpath.endswith(".exe"):
            binpath = binpath + ".exe"
        title = POPUP_TITLE
        status = sc.create_shortcut(binpath, title, "一个方便的抽奖工具")
        if status:
            mb.showinfo(POPUP_TITLE, "【" + title + "】快捷方式创建成功！")
        else:
            mb.showerror(POPUP_TITLE, "抱歉，当前系统不支持创建快捷方式。")
    else:
        mb.showinfo(POPUP_TITLE, "抱歉，仅支持Windows系统创建快捷方式！")



def trigger_upgrade():
    upgrade()


def show_about():
    message = """
操作说明：
界面从上到下。
极简开发工具
有其他改进建议可以找qq：【Python全栈技术学习交流】：https://jq.qq.com/?_wv=1027&k=ISjeG32x 
    """
    mb.showinfo(POPUP_TITLE, message)



