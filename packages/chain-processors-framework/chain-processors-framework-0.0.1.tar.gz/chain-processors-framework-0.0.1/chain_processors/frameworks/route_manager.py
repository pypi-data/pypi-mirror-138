#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 4:21 下午
# @File    : route_manager.py
# @author  : byscut
import sys
import logging
from chain_processors.frameworks.processor_chains import ProcessorChains

logger = logging.getLogger(__name__)


class RouteManager(object):
    def __init__(self):
        pass

    @staticmethod
    def select_router(config_path, file_type='local', project_root='.'):
        if project_root not in list(sys.path):
            sys.path.append(project_root)
            logger.info("WORK DIRCTORY：{}".format(sys.path))
        route = ProcessorChains(config_path, file_type=file_type)
        return route


if __name__ == '__main__':
    route = RouteManager.select_router('../test.json')
    obj = route.process(['00001000001'])
    print(obj)
