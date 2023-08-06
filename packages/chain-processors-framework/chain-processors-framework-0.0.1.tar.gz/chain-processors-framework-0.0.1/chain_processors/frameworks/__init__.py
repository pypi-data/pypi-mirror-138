#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 2:42 下午
# @File    : __init__.py.py
# @author  : byscut


class Config:
    CONFIG_FILE_SOURCE_REMOTE = 'remote'
    CONFIG_FILE_SOURCE_LOCAL = 'local'

    IO_TYPE_SINGLE = 'single'
    IO_TYPE_LIST = 'list'

    DIRECT_RETURN_CLASS_NAME = 'r'


from chain_processors.frameworks.route_manager import RouteManager
from chain_processors.frameworks.processor import Processor
from chain_processors.frameworks.context_manager import ContextManager
from chain_processors.frameworks.processor_chains import ProcessorChains
