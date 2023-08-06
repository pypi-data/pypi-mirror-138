#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 4:48 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : new_item_handler.py
# @Project : icode
import os
import pathlib
from tkinter import *
from tkinter import ttk

from codelife import notification, store
from codelife.core import tree_node_render
from codelife.generator.generator_factory import GeneratorFactory
from codelife.tree import FileItem


def create_panel(root, treeview):
    secondary = Toplevel(master=root,
                         background="lightblue", padx=4, pady=4)
    secondary.title("New File/Folder")
    secondary.geometry("300x100")
    filetype = Label(secondary, text="FileType", background="lightblue")
    filetype_var = StringVar()
    combobox = ttk.Combobox(secondary, textvariable=filetype_var)
    combobox['value'] = ("Python", "Python Module", "Folder", "Text")
    combobox.set(combobox['value'][0])
    filetype.grid(row=0, column=0, sticky=NSEW)
    combobox.grid(row=0, column=1, sticky=NSEW)
    filename = Label(secondary, text="FileName", background="lightblue")
    filename_value = Entry(secondary)
    filename.grid(row=1, column=0, sticky=NSEW)
    filename_value.grid(row=1, column=1, sticky=NSEW)
    group = PanedWindow(master=secondary, background="lightblue")
    group.columnconfigure(0, weight=1, pad=1)
    group.columnconfigure(1, weight=1, pad=1)

    def on_closing():
        try:
            secondary.destroy()
        finally:
            # PRIZE_META['pickerWinOpen'] = False
            pass

    def create_new_item():
        file_type = filetype_var.get()
        if file_type is None or file_type.strip() == "":
            notification.alert("Please select/input a valid type")
        file_type = file_type.strip()
        filename_text = filename_value.get()
        if filename_text is None or filename_text.strip() == "":
            notification.alert("Please select/input a valid file name")
            return
        item = treeview.selection()
        # print("selection ", item, type(item))
        if item is None or len(item) == 0:
            notification.alert("Please click to select any project folder first!")
            return
        else:
            project = store.get_current_project()
            active_dir = store.get_active_dir()
            active_dir = active_dir if active_dir is not None else project
            #print("filename:", filename_text, ", active dir:", active_dir)
            full_file_name = os.path.join(active_dir, filename_text)
            if file_type == "Python":
                if not full_file_name.endswith(".py"):
                    full_file_name += ".py"
                    filename_text += ".py"
            final_path = pathlib.Path(full_file_name)
            if final_path.exists():
                notification.alert("Already exist for file " + full_file_name)
                return
            # print("will create ", full_file_name)
            if file_type == 'Folder':
                final_path.mkdir()
            else:
                # print("type:", file_type)
                g = GeneratorFactory().get_generator(file_type)
                g.generate(full_file_name)
            item_value = treeview.item(item)
            # print("item:", item_value)
            current_item = item[0]
            level = tree_node_render.extract_level(current_item)
            folder = tree_node_render.extract_folder(current_item)
            #print("folder:", folder)
            if os.path.isdir(folder):
                level = int(level) + 1
                new_node = tree_node_render.add_node(treeview, current_item, filename_text, full_file_name, level)
                if file_type == 'Folder':
                    tree_node_render.tag_folder_node(treeview, new_node)
            else:
                parent_folder = os.path.abspath(os.path.join(folder, os.pardir))
                parent_filename_text = os.path.basename(parent_folder)
                level = int(level) - 1
                fitem = FileItem(name=parent_filename_text, path=parent_folder, level=level)
                node_key = tree_node_render.get_node_key(fitem)
                #print("node_key:",node_key)
                level = int(level) + 1
                new_node = tree_node_render.add_node(treeview, node_key, filename_text, full_file_name, level)
                if file_type == 'Folder':
                    tree_node_render.tag_folder_node(treeview, new_node)
        notification.msg(full_file_name + " created!")
        on_closing()

    ok_button = Button(group, text="Ok", width=10, command=create_new_item)
    cancel_button = Button(group, text="Cancel", width=10, command=on_closing)
    ok_button.grid(row=0, column=0, sticky=NSEW)
    cancel_button.grid(row=0, column=1, sticky=NSEW)
    group.grid(row=2, column=1, sticky=NSEW)
    secondary.rowconfigure(0, weight=1, pad=1)
    secondary.rowconfigure(1, weight=1, pad=1)
    secondary.rowconfigure(2, weight=1, pad=1)
    secondary.columnconfigure(0, weight=1, pad=1)
    secondary.columnconfigure(1, weight=1, pad=1)

    secondary.protocol("WM_DELETE_WINDOW", on_closing)
