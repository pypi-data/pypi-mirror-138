#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 9:01 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : python_file_generator.py
# @Project : codelife
from codelife.generator.generator import Generator


class DummyGenerator(Generator):
    def generate(self, output_path: str):
        return None
