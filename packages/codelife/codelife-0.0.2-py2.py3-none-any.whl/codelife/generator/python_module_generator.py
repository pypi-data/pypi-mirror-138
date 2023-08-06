#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 11:57 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : python_module_generator.py
# @Project : codelife
import os
import pathlib

from codelife.generator.generator import Generator


class PythonModuleGenerator(Generator):
    def generate(self, output_path):
        p = pathlib.Path(output_path)
        p.mkdir()
        init_file = os.path.join(output_path, "__init__.py")
        with open(init_file, 'w') as f:
            data = """# -*- coding: utf-8 -*-

"""
            f.write(data)
