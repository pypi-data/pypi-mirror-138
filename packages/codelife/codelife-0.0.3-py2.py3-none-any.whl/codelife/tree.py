#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/25 22:20 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : tree.py
# @Project : codelife
import os


class Node(object):
    def __init__(self, value, parent=None, children=None):
        # print("value=", value)
        # print("parent=", parent)
        # print("type parent=", type(parent))
        self._value = value
        self._parent = parent
        self._children = children if children else []

    def has_child(self):
        if self._children is Node:
            return False
        lens = len(self._children)
        return lens > 0

    def get_children(self):
        if self.has_child():
            return [x for x in self._children]
        return []

    def add_child(self, node):
        self._children.append(node)

    def get_value(self):
        return self._value

    def __str__(self):
        # print("type self.parent=", type(self.parent))
        try:
            parent_name = self._parent.get_value()[2] if self._parent else 'N/A'
        except Exception as err:
            parent_name = self._parent.get_value() if self._parent else 'N/A'
        children = ",".join([str(x) for x in self._children]) if self._children else '[]'
        return f"Node( value: {self._value} , parent: {parent_name},\n children: {children})"


class Tree(object):
    def __init__(self):
        self.nodes = []

    def add(self, node: Node):
        self.nodes.append(node)

    def __str__(self):
        nodes = ",".join([str(x) for x in self.nodes])
        return f"Tree( nodes: {nodes})"


class FileItem(object):
    def __init__(self, name, path, level):
        self._name = name
        self._path = path
        self._level = level

    def get_name(self):
        return self._name

    def get_path(self):
        return self._path

    def get_level(self):
        return self._level

    def __str__(self):
        return f"FileItem( name: {self._name}, level: {self._level})"



def build_file_tree(file, depth=0, parent=None):
    filename = os.path.basename(file)
    cur_node = Node(value=FileItem(path=file, level=depth, name=filename), parent=parent)
    if os.path.isfile(file):
        return cur_node
    else:
        sub_files = os.listdir(file)
        parent_ent = cur_node
        for sf in sub_files:
            sf_path = os.path.join(file, sf)
            parent_ent.add_child(build_file_tree(sf_path, depth + 1, parent_ent))
        return parent_ent


if __name__ == "__main__":
    t = Tree()
    t.add(Node('', ('/Users/mac/PycharmProjects/icode', 0, 'icode', 'node')))
    subTree = Tree()

    # t.add(Node('/Users/mac/PycharmProjects/icode',Node('/Users/mac/PycharmProjects/icode/icode', 1, 'icode', 'subTree')))
    # print(t)
    root = Node(('/Users/mac/PycharmProjects/icode', 0, 'icode', 'node'))
    icode = Node(('/Users/mac/PycharmProjects/icode/icode', 1, 'icode', 'node'), root)
    icode = Node(value=('/Users/mac/PycharmProjects/icode/zz', 1, 'zz', 'node'), parent=root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root=", root)
    print("root type ", type(root))
    print("root value ", root.get_value())
    print("icode=", icode)
    fsTree = build_file_tree('/codelife')




