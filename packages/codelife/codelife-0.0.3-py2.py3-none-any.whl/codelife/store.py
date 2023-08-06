#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 2:00 上午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : store.py
# @Project : codelife
import queue

stat = {
    "event_loop": queue.LifoQueue()
}


def get_stat():
    return stat


def register_event(event, args):
    #print("register event:", event, ", args:", args)
    e = {
        "event": event,
        "args": args
    }
    stat['current_event'] = e
    stat['event-' + event] = e
    stat['event_loop'].put(e)


def get_current_project():
    # return stat['set_project'] if 'set_project' in stat else None
    e = get_event_stat('set_project')
    if e:
        return e['args']
    else:
        None


def get_active_dir():
    # return stat['set_active_dir'] if 'set_active_dir' in stat else None
    e = get_event_stat('set_active_dir')
    if e:
        return e['args']
    else:
        None


def get_event_stat(event):
    return stat['event-' + event] if 'event-' + event in stat else None






















