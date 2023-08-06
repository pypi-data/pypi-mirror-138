#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 10:54 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : text_decorator.py
# @Project : codelife
from tkinter import Text


def error_tag():
    return 'tag_error'


def decorate_error(component: Text):
    component.tag_config(error_tag(), foreground='red')
