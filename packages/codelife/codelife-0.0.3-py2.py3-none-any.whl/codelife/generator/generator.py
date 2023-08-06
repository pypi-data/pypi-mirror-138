#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 9:17 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : generator.py
# @Project : codelife


import abc


class Generator(abc.ABC):
    @abc.abstractmethod
    def generate(self,output_path:str):
        pass
