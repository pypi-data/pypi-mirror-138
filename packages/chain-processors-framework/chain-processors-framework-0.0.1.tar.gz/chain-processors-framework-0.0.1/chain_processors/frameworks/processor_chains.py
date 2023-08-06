#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 10:18 上午
# @File    : processor_chains.py
# @author  : byscut
import traceback
import logging
import copy
import time
import json
import importlib
from collections import defaultdict, deque
from chain_processors.frameworks.context_manager import ContextManager
from chain_processors.frameworks import Config

logger = logging.getLogger(__name__)


class ProcessorChains(object):
    def __init__(self, conf_path, **kwargs):
        # 初始化要用到的插件
        file_type = kwargs.get('file_type', Config.CONFIG_FILE_SOURCE_LOCAL)
        self.conf = None
        if file_type == Config.CONFIG_FILE_SOURCE_REMOTE:
            raise Exception("not supporting temporarily")
        else:
            self.conf = json.load(open(conf_path, 'r'))

        self.processors = []
        self.plugin_configs = {}
        self.output_conf = self.conf.get('output', {})
        self.input_conf = self.conf.get('input', {})

        self._check_conf()
        for processor in self.conf.get('processors', []):
            self.plugin_configs[processor['name']] = processor
            Processor = self.get_processor_cls(processor['path'])
            self.processors.append(Processor(processor['name'], **processor['args']))
        logger.info("Processor = {}".format(self.processors))
        self.methods = defaultdict(deque)
        for processor in self.processors:
            self._add_processor(processor)
        logger.info("FINISH ADDING PROCESSOR...")

    def _check_conf(self):
        input_name = self.input_conf.get('name', 'inputs')
        if not input_name or '-' in input_name or '.' in input_name:
            raise Exception("【配置文件异常】INPUT名称不合法！不能包含字符-或者点字符，input = {}".find(input_name))
        if len(input_name) < 2:
            raise Exception("【配置文件异常】INPUT名称不合法！名称长度至少为2，input = {}".find(input_name))

        for item in self.conf.get('processors', []):
            name = item.get('name')
            if not name or '-' in name or '.' in name:
                raise Exception("【配置文件异常】Processor名称不合法！不能包含字符-或者点字符，name = {}".find(name))
            if len(name) < 2:
                raise Exception("【配置文件异常】Processor名称不合法！名称长度至少为2，name = {}".find(name))

    @staticmethod
    def get_processor_cls(module_str):
        paths = module_str.split('.')
        class_name = paths[-1]
        module_path = '.'.join(paths[:-1])
        plugin_mod = importlib.import_module(module_path)
        PluginCls = getattr(plugin_mod, class_name)
        if not PluginCls:
            raise Exception('User defined plugin %s not exists' % module_str)
        return PluginCls

    def _add_processor(self, processor):
        if hasattr(processor, 'process'):
            self.methods['process'].append(processor.process)

    def judge_type_copy(self, input):
        '''
        判断输入是什么类型，如果是df则不需要复制，如果是dict，list类型则需要进行深复制
        '''
        if isinstance(input, dict) or isinstance(input, list) or isinstance(input, str):
            return copy.deepcopy(input)
        return input

    def process(self, inputs, context: ContextManager=None):
        # 先写成代码自定义流程，然后改写成配置文件形式
        # 输入为上游传进来的data，输出为要传给下游的data，如果没有下游数据则返回false（或者空数据）即可
        # 中间数据格式是自定义，要和自定义插件格式保持一致
        logger.info("data input")
        if context is None or not isinstance(context, ContextManager):
            if context is not None:
                logger.error("input context format error, use empty context..")
            context = ContextManager()

        def process_chain(inputs: list, context: ContextManager):
            middles = inputs
            context.add_context(self.input_conf.get('name', 'inputs'), middles)
            for method in self.methods['process']:
                begin_time = time.time()
                middles, class_name = method(inputs=self.judge_type_copy(middles), context=context)
                logger.info('method {}.process use time: {} s'.format(class_name, time.time() - begin_time))
                context.add_context(class_name, middles)
                # 如果遇到特殊情况要直接返回，将函数第二个返回值设为对应值，则不再执行后续
                if class_name == Config.DIRECT_RETURN_CLASS_NAME:
                    break
            outputs = middles
            return outputs

        try:
            if self.input_conf:
                if self.input_conf.get('type', Config.IO_TYPE_LIST) == Config.IO_TYPE_SINGLE or not isinstance(inputs, list):
                    inputs = [inputs]
            outputs = process_chain(inputs, context)
            if self.output_conf:
                if self.output_conf.get('type', Config.IO_TYPE_LIST) == Config.IO_TYPE_SINGLE and len(outputs) > 0:
                    outputs = outputs[0]
        except Exception as e:
            logger.error(traceback.format_exc())
            return None

        return outputs


if __name__ == '__main__':
    plugins = ProcessorChains('../test.json')
    obj = plugins.process(['00001000001', 'simple'])
    print(obj)
