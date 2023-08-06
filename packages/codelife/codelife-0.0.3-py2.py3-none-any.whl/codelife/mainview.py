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
import pathlib
import threading
import tkinter
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter.ttk import Treeview

from codelife import loopfiles, tree, store, notification
from codelife.common.text_decorator import decorate_error
from codelife.core import tree_node_render
from codelife.event_handler import handle_saving_event
from codelife.menu_setting import show_copyright, show_about, trigger_upgrade, make_shortcut
from codelife.project_item_creator import create_panel
from codelife.setting import LABEL
from codelife.proxy_run import run_python
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
        self.render_project(curdir, treeview)

    def render_project(self, curdir, treeview):
        fstree: Node = tree.build_file_tree(curdir)
        # print("scan_file_tree=", fstree)
        try:
            store.register_event('set_project', curdir)
            self.render_fs_tree(fstree, treeview, None)
        except Exception as err:
            # logging.error(err)
            print("error:", err)
            raise err

    def render_fs_tree(self, node: Node, treeview: Treeview, root_node: Node):
        t_item: FileItem = node.get_value()
        current_item = "" if root_node is None else root_node
        new_node = tree_node_render.add_node(treeview, current_item, t_item.get_name(), t_item.get_path(),
                                             t_item.get_level())
        if node.has_child():
            for sub_node in node.get_children():
                tree_node_render.tag_folder_node(treeview, new_node)
                self.render_fs_tree(sub_node, treeview, new_node)

    def build_file_tree(self):
        treeview = ttk.Treeview(self.root)
        self.treeview = treeview
        tree_node_render.decorate_tree(treeview)

        def handle_fs_tree_event(event):
            item = treeview.selection()
            if item:
                item_value = treeview.item(item)
                # print('click item:', item, ' text: ', item_value)
                file_path = item_value['values'][0]
                if os.path.isdir(file_path):
                    store.register_event("set_active_dir", file_path)
                    return
                with open(file_path, 'r') as f:
                    store.register_event('editing', file_path)
                    self.entry_file.delete(1.0, END)
                    self.entry_file.insert(INSERT, f.read())
                    self.console['value'].grid_forget()
                    self.console['value_scroll'].grid_forget()
                    self.right_panel.update()

        treeview.bind('<ButtonRelease-1>', handle_fs_tree_event)

        def right_key_event(event):
            print("right_click")

        treeview.bind('<Button-3>', right_key_event)
        treeview.grid(row=1, column=0, sticky=NS)
        self.render_local_dirtree(treeview)

    def build_editor_panel(self):
        right_panel = PanedWindow(master=self.root)
        entry_file = Text(right_panel, background='lightblue')
        scroll = Scrollbar(master=right_panel)
        # associate the text and scroll bar
        scroll.config(command=entry_file.yview)
        entry_file.config(yscrollcommand=scroll.set)
        entry_file.grid(row=0, column=0, sticky=NSEW)
        scroll.grid(row=0, column=1, sticky=NSEW)

        right_panel.grid(row=1, column=1, sticky=NSEW)
        right_panel.rowconfigure(0, weight=1, pad=1)
        right_panel.columnconfigure(0, weight=1, pad=1)
        console = Text(right_panel, background='lightyellow')
        decorate_error(console)
        console_scroll = Scrollbar(master=right_panel)
        # associate the text and scroll bar
        console_scroll.config(command=console.yview)
        console.config(yscrollcommand=console_scroll.set)
        self.console['value'] = console
        self.console['value_scroll'] = console_scroll
        self.right_panel = right_panel
        self.entry_file = entry_file

    def setup(self):
        root = self.root
        self.console = {}
        root.geometry('776x666')
        root.title(LABEL)
        BG_COLOR = 'skyblue'
        root.configure(bg=BG_COLOR)
        root.config(menu=self.construct_menu())
        label = ttk.Label(root, text="Project")
        label.grid(row=0, column=0, sticky=NSEW)
        banner = ttk.Panedwindow(orient=tkinter.HORIZONTAL)

        def save_code():
            # print("save code:")
            editor_content = self.entry_file.get('1.0', END)
            store.register_event('saving', editor_content)
            handle_saving_event()

        save_btn = ttk.Button(banner, text="Save", command=save_code)

        def explore_file():
            # print("explore_file code:")
            file_path = askdirectory()
            if file_path:
                self.render_project(file_path, self.treeview)

        def new_file():
            create_panel(self.root, self.treeview)

        open_project_btn = ttk.Button(banner, text="Open", command=explore_file)
        new_item_btn = ttk.Button(banner, text="New", command=new_file)

        def run_code():
            # print("run code:")
            e = store.get_event_stat('editing')
            if e:
                save_code()

                # print("e:", e)

                def trigger_run():
                    console = self.console['value']
                    console_scroll = self.console['value_scroll']
                    console.delete(1.0, END)
                    console.grid(row=1, column=0, sticky=NSEW)
                    console_scroll.grid(row=1, column=1, sticky=NSEW)
                    run_python("python3 " + e['args'], console)

                t = threading.Thread(target=trigger_run)
                t.setDaemon(True)
                t.start()

        run_btn = ttk.Button(banner, text="Run", command=run_code)
        counter = 0
        open_project_btn.grid(row=0, column=counter, sticky=NSEW)
        counter += 1
        new_item_btn.grid(row=0, column=counter, sticky=NSEW)
        counter += 1
        save_btn.grid(row=0, column=counter, sticky=NSEW)
        counter += 1
        run_btn.grid(row=0, column=counter, sticky=NSEW)
        counter += 1

        banner.grid(row=0, column=1, sticky=NSEW)
        # self.root.rowconfigure(0, weight=1, pad=1)
        self.root.rowconfigure(1, weight=1, pad=1)
        # self.root.columnconfigure(0, weight=1, pad=1)
        self.root.columnconfigure(1, weight=1, pad=1)
        self.build_file_tree()
        self.build_editor_panel()

    def start_app(self):
        self.root.mainloop()


if __name__ == "__main__":
    MainView().start_app()
