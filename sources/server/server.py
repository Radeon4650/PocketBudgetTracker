# -*- coding: utf-8 -*-
"""
Copyright © 2018 PocketBudgetTracker. All rights reserverd.
Author: Approximator (alex@nls.la)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

import tornado
from tornado.web import RequestHandler, Application
from db import NativeCoroutinesRequestHandler, GenCoroutinesRequestHandler, SynchronousRequestHandler, make_db

# pylint: disable=arguments-differ,abstract-method
logger = logging.getLogger('server')  # pylint: disable=invalid-name
logging.getLogger('tornado').setLevel(logging.WARNING)


class MainHandler(RequestHandler):
    """
    Handler for the GET / request
    """

    def get(self):
        self.write("<h3>Hello, Here is PocketBudgetTracker</h3>")


class PBTServer:
    """
    Server
    """

    def __init__(self):
        self._listen_ip = '127.0.0.1'
        self._listen_port = 8788

        self._session_factory = make_db('sqlite:////tmp/pbt_test.db')

        routes = [
            (r'/', MainHandler),
            (r'/native-coroutines', NativeCoroutinesRequestHandler),
            (r'/gen-coroutines', GenCoroutinesRequestHandler),
            (r'/sync', SynchronousRequestHandler),
        ]

        self._app = Application(
            routes, session_factory=self._session_factory).listen(self._listen_port, self._listen_ip)

    def run(self):
        """
        Start server on a specific ip:port
        """
        logger.info('The server is listening on {}:{}'.format(self._listen_ip, self._listen_port))
        tornado.ioloop.IOLoop.current().start()
