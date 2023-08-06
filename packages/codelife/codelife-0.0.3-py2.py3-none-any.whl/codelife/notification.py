#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 4:38 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : notification.py
# @Project : codelife

import tkinter.messagebox as mb

from codelife.menu_setting import POPUP_TITLE


def alert(msg):
    mb.showerror(POPUP_TITLE, msg)

def msg(msg):
    mb.showinfo(POPUP_TITLE, msg)

