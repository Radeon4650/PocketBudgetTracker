# -*- coding: utf-8 -*-
"""
Copyright © 2018 PocketBudgetTracker. All rights reserved.
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

import os
import tornado
from tornado.web import Application

import db
from config import PbtConfig
from .handlers import get_all_routes

# pylint: disable=arguments-differ,abstract-method
logger = logging.getLogger('server')  # pylint: disable=invalid-name
logging.getLogger('tornado').setLevel(logging.WARNING)


class PBTServer:
    """
    Server
    """

    def __init__(self):
        self._config = PbtConfig()
        self._config.load()

        self._session_factory = db.make_db(self._config.db_path())

        self._app = Application(get_all_routes(),
                                session_factory=self._session_factory,
                                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                static_path=os.path.join(os.path.dirname(__file__), "static"),
                                login_url="/auth/login",
                                cookie_secret="pbt_debug_secret")
        self._app.listen(self._config.port(), self._config.host())

    def run(self):
        """
        Start server on a specific ip:port
        """
        logger.info('The server is listening on http://%s:%d', self._config.host(), self._config.port())
        tornado.ioloop.IOLoop.current().start()
