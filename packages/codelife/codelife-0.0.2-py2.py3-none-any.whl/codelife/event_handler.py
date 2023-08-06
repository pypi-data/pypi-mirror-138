#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 2:14 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : event_handler.py.py
# @Project : codelife
from codelife import store


def handle_saving_event():
    #print("save code:")
    editing_stat = store.get_event_stat('editing')
    saving_stat = store.get_event_stat('saving')
    if saving_stat and editing_stat:
        file_path = editing_stat['args']
        content = saving_stat['args']
        #print("file_path:", file_path)
        #print("content:", content)
        with open(file_path, 'w') as f:
            f.write(content)
    else:
        print("do nothing")
