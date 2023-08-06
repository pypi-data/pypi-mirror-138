#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/11 2:52 下午
# @File    : recall_processor.py
# @author  : byscut
# this example must run pip install elasticsearch first
import elasticsearch
from chain_processors.frameworks.processor import Processor


class RecallProcessor(Processor):
    def __init__(self, name, **kwargs):
        super(RecallProcessor, self).__init__(name, **kwargs)
        self.es_host = kwargs.get('es_host')
        self.es_index = kwargs.get('es_index', {})
        self.es_client = elasticsearch.Elasticsearch(self.es_host)

        assert self.es_index != {}, "无法获取es索引名称"

    def process(self, inputs, context=None):
        return_list = []
        for data in inputs:
            query_body = self.make_query_body(data)
            es_result = self.es_client.search(index=self.es_index, body=query_body)
            return_list.append(es_result)

        return return_list, self.name

    def make_query_body(self, data):
        """ 从query生成符合es的查询体

        Arguments:
            data: 输入的字典类型的查询请求.

        Returns:
            query_body: 使用data构造的es查询体.

        Raises:
            InvalidArgumentError
        """
        raise NotImplementedError(
            'Subclasses should implement the predict func')
