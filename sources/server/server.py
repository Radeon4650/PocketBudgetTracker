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

from db import make_db
from .handlers import routes

# pylint: disable=arguments-differ,abstract-method
logger = logging.getLogger('server')  # pylint: disable=invalid-name
logging.getLogger('tornado').setLevel(logging.WARNING)


class PBTServer:
    """
    Server
    """

    def __init__(self, ip, port, db_path):
        self._listen_ip = ip
        self._listen_port = port

        self._session_factory = make_db(db_path)

        self._app = Application(routes, session_factory=self._session_factory)
        self._app.listen(self._listen_port, self._listen_ip)

    def run(self):
        """
        Start server on a specific ip:port
        """
        logger.info('The server is listening on {}:{}'.format(self._listen_ip, self._listen_port))
        tornado.ioloop.IOLoop.current().start()
