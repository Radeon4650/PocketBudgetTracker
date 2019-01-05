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
import sys
import alembic.config as aconf
from config import PbtConfig

ALEMBIC_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'alembic.ini')


def upgrade(config):
    run_alembic(config, ['upgrade', 'head'])


def run_alembic(config, args=[]):
    alembic_args = ['-c', ALEMBIC_CONFIG_PATH, '-x', "dbPath={}".format(config.db_path()), '--raiseerr']
    alembic_args += args
    aconf.main(alembic_args)


if __name__ == '__main__':
    appConf = PbtConfig()
    appConf.load()
    run_alembic(appConf, sys.argv[1:])
