#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 2:00 上午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo


import logging
import shutil
import subprocess
import sys
import threading
from tkinter import *

from codelife.common.text_decorator import error_tag


def run_python(cmd, console):
    # print("will run cmd:", cmd)
    cmd_path = shutil.which("sh")
    cmd_path = cmd_path + " " + cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # p.wait()
    def render_console():
        lines = p.stdout.readlines()
        error = p.stderr.readlines() if p.stderr else None
        # print("exec:", lines,type(lines))
        console.delete(1.0, END)
        if lines is None:
            lines = []
        lines.append('')
        lines.append("Process finished with code " + str(p.wait()))
        line_no = len(lines)
        lines_str = "\n".join([x.decode() if type(x) == bytes else x for x in lines])
        console.insert(INSERT, lines_str)
        if error:
            lines_str = "\n".join([x.decode() if type(x) == bytes else x for x in error])
            console.insert(str(line_no) + ".0", lines_str, error_tag())

    t = threading.Thread(target=render_console)
    t.setDaemon(True)
    t.start()
    return None



