#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/11 2:51 下午
# @File    : query_processor.py
# @author  : byscut
from chain_processors.frameworks.processor import Processor


class QueryProcessor(Processor):
    def __init__(self, name, **kwargs):
        super(QueryProcessor, self).__init__(name, **kwargs)

    def process(self, inputs, context=None):
        # 对query不做什么事情，要修改则继承该类重写process方法
        outputs = inputs
        return outputs, self.name
