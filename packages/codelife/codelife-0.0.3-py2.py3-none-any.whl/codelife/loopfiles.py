#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/02/13 12:19 上午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : loopfiles.py
# @Project : codelife

import os


def scan_files(file):
    if os.path.isfile(file):
        return [file]
    else:
        sub_files = os.listdir(file)
        entries = [file]
        for sf in sub_files:
            sf_path = os.path.join(file, sf)
            entries += scan_files(sf_path)
        return entries


def scan_file_tree(file, depth=0):
    if os.path.isfile(file):
        return [(file, depth, os.path.basename(file))]
    else:
        sub_files = os.listdir(file)
        entries = [(file, depth, os.path.basename(file))]
        for sf in sub_files:
            sf_path = os.path.join(file, sf)
            entries += scan_file_tree(sf_path, depth + 1)
        return entries


if __name__ == "__main__":
    curdir = "/Users/mac/PycharmProjects/icode/codelife"
    files = scan_file_tree(curdir)
    print("files=", files)
    from tkinter import *
    from tkinter.ttk import *

    root = Tk()
    treeview = Treeview(root)
    treeview.grid(row=1, column=0, sticky=N + S)

    for x in files:
        depth = x[1]
        name = x[2]
        if depth == 0:
            treeview.insert("", str(depth), "i%s" % (depth+1), text=name)
        else:
            treeview.insert("i%s" % depth, str(depth), "i%s" % depth, text=name)
    root.mainloop()















