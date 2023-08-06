#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 10:16 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : tree_node_render.py
# @Project : codelife
import time
import uuid
from tkinter.ttk import Treeview

from codelife.tree import FileItem


class TreeNodeStat():
    _PRIVATE_STAT = {}


def get_folder_tag():
    return 'tag_folder'


def tag_folder_node(treeview: Treeview, node):
    treeview.item(node, tags=(get_folder_tag()))


def decorate_tree(treeview: Treeview):
    treeview.tag_configure('tag_folder', background='lightblue')


def add_node(treeview: Treeview, parent_node, filename_text: str, full_file_name: str, level: int):
    fitem = FileItem(name=filename_text, path=full_file_name, level=level)
    node_key = generate_node_key(fitem)
    new_node = treeview.insert(parent_node, fitem.get_level(), node_key, text=fitem.get_name(),
                               values=(fitem.get_path()))
    return new_node


def extract_level(node_key):
    node_value = TreeNodeStat._PRIVATE_STAT[node_key]
    return node_value.split("@")[0]


def extract_folder(node_key):
    node_value = TreeNodeStat._PRIVATE_STAT[node_key]
    index = node_value.index('/')
    return node_value[index + 1:]


def get_node_key(fitem: FileItem):
    fname = fitem.get_name()
    if '/' in fname:
        fname.replace('/', '_')
    value = str(fitem.get_level()) + "@" + fname + str(fitem.get_level()) + "/" + fitem.get_path()
    for k, v in TreeNodeStat._PRIVATE_STAT.items():
        if v == value:
            return k
    return None


def generate_node_key(fitem: FileItem):
    fname = fitem.get_name()
    if '/' in fname:
        fname.replace('/', '_')
    # key contains chinese text may cause issue when treeview.item( given item key)
    # return str(fitem.get_level()) + "@" + fname + str(fitem.get_level()) + "/" + fitem.get_path()
    value = str(fitem.get_level()) + "@" + fname + str(fitem.get_level()) + "/" + fitem.get_path()
    key = str(uuid.uuid4()) + str(time.time())
    TreeNodeStat._PRIVATE_STAT[key] = value
    return key
