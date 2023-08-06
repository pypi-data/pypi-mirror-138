#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 4:25 下午
# @File    : run.py
# @author  : Bai
import logging
from chain_processors import RouteManager, ContextManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, *args, **kwargs):
        super(Runner, self).__init__(*args, **kwargs)
        self.route = RouteManager.select_router('test.json', file_type='local')

    def predict(self, data, **kwargs):
        logger.info('### runner.predicting ###')
        print("{}, {}, {}".format("### CHECK-DATA ###", data, type(data)))
        context = ContextManager()
        context.add_context('udf_string', ' - 自定义的字符串')
        if not data:
            return
        outputs = self.route.process(data, context)
        return outputs


if __name__ == '__main__':
    model = Runner()
    result = model.predict(['1010111', 'simple'])
    print(result)
