#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright © 2019 PocketBudgetTracker. All rights reserved.
Author: Andrey Shelest (khadsl1305@gmail.com)

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


import os
import logging
import alembic.config as aconf
from alembic import command

logger = logging.getLogger('pbt.migrate')
logging.getLogger('alembic').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


class Migrate:
    def __init__(self, db_path, directory='migrations', ini_file='alembic.ini'):

        self.db_path = db_path
        self.directory = os.path.join(os.path.dirname(__file__), directory)
        self.ini_path = os.path.join(os.path.dirname(__file__), ini_file)
        self.config = aconf.Config(file_=None)
        self.config.set_main_option('script_location', self.directory)
        self.config.set_main_option('sqlalchemy.url', self.db_path)

    def print_info(self):
        print('DataBase url is {}'.format(self.db_path))
        command.show(self.config, 'current')

    def upgrade_head(self):
        logger.info('Database upgrade started.')
        command.upgrade(self.config, 'head')
        logger.info('Database upgrade finished.')

    def commit(self, msg):
        command.revision(self.config, message=msg, autogenerate=True)
