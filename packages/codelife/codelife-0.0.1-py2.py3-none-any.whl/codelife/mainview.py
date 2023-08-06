#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/24 11:00 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : treeview.py
# @Project : codelife
import logging
import os
from tkinter import *
from tkinter import ttk

from codelife import loopfiles, tree
from codelife.menu_setting import show_copyright, show_about, trigger_upgrade, make_shortcut
from codelife.setting import LABEL
from codelife.tree import Node, FileItem


class MainView(object):
    def __init__(self):
        self.root = Tk()
        self.setup()

    def construct_menu(self):
        menu_bar = Menu(self.root)
        about_menu = Menu(menu_bar)
        setting_menu = Menu(menu_bar)
        about_menu.add_command(label='版权信息', command=show_copyright)
        about_menu.add_command(label='操作说明', command=show_about)
        about_menu.add_command(label='升级', command=trigger_upgrade)
        setting_menu.add_command(label='创建桌面快捷方式', command=make_shortcut)
        menu_bar.add_cascade(label="使用介绍", menu=about_menu)
        menu_bar.add_cascade(label="更多配置", menu=setting_menu)
        return menu_bar

    def render_local_dirtree(self, treeview):
        import os
        curdir = os.getcwd()
        #curdir = "/Users/mac/PycharmProjects/icode"
        fstree: Node = tree.build_file_tree(curdir)
        #print("scan_file_tree=", fstree)
        try:
            self.render_tree(fstree, treeview)
        except Exception as err:
            # logging.error(err)
            print("error:", err)
            raise err
        pass

    def render_tree(self, fstree: Node, treeview):
        node = fstree
        self.render_fs_tree(node, treeview, None)

    def render_fs_tree(self, node, treeview, root_node):
        fitem: FileItem = node._value
        item_label = fitem.get_name() + str(fitem.get_level()) + fitem.get_path()
        if root_node is None:
            root = treeview.insert("", fitem.get_level(), item_label, text=fitem.get_name(),
                                   values=(fitem.get_path()))
        else:
            root = treeview.insert(root_node, fitem.get_level(), item_label, text=fitem.get_name(),
                                   values=(fitem.get_path()))
        if node.has_child():
            for sub_node in node.get_children():
                self.render_fs_tree(sub_node, treeview, root)

    def build_file_tree(self):
        treeview = ttk.Treeview(self.root)

        def handle_fs_tree_event(event):
            item = treeview.selection()
            if item:
                item_value = treeview.item(item)
                print('click item:', item, ' text: ', item_value)
                file_path = item_value['values'][0]
                if os.path.isdir(file_path):
                    return
                with open(file_path,'r') as f:
                    self.entry_file.delete(1.0,END)
                    self.entry_file.insert(INSERT, f.read())

        treeview.bind('<ButtonRelease-1>', handle_fs_tree_event)
        treeview.grid(row=1, column=0, sticky=N + S)
        self.render_local_dirtree(treeview)

    def build_editor_panel(self):
        entry_file = Text(self.root,background='skyblue')
        entry_file.grid(row=1, column=1, sticky=W + E + N + S)
        self.entry_file = entry_file

    def setup(self):
        root = self.root
        root.geometry('776x333')
        root.title(LABEL)
        BG_COLOR = 'skyblue'
        root.configure(bg=BG_COLOR)
        self.construct_menu()
        label = ttk.Label(root, text="Project")
        label.grid(row=0, column=0, sticky=NSEW)
        banner = ttk.Label(root, text="")
        banner.grid(row=0, column=1, sticky=NSEW)
        #self.root.rowconfigure(0, weight=1, pad=1)
        self.root.rowconfigure(1, weight=1, pad=1)
        #self.root.columnconfigure(0, weight=1, pad=1)
        self.root.columnconfigure(1, weight=1, pad=1)
        self.build_file_tree()
        self.build_editor_panel()

    def start_app(self):
        self.root.mainloop()


if __name__ == "__main__":
    MainView().start_app()
