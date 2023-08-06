#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/2/13 8:57 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : generator_factory.py
# @Project : codelife


from codelife.generator.dummy_generator import DummyGenerator
from codelife.generator.python_file_generator import PythonFileGenerator
from codelife.generator.python_module_generator import PythonModuleGenerator
from codelife.generator.text_file_generator import TextFileGenerator

GENERATOR_DICT = {
    "PYTHON": PythonFileGenerator(),
    "PYTHON MODULE": PythonModuleGenerator(),
    "TEXT": TextFileGenerator(),
    "DUMMY": DummyGenerator(),
}


class GeneratorFactory():
    def get_generator(self, file_type: str):
        if file_type is None:
            return DummyGenerator()
        else:
            file_type = str(file_type).upper()
            return GENERATOR_DICT[file_type]


if __name__ == "__main__":
    GeneratorFactory().get_generator("DUMMY").generate('/tmp')
