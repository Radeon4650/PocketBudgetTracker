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

import argparse
import logging
from db import Migrate
from config import PbtConfig

logging.getLogger('pbt').setLevel(logging.INFO)

if __name__ == '__main__':
    appConf = PbtConfig()
    appConf.load()

    db_migrate = Migrate(appConf.db_path())

    parser = argparse.ArgumentParser(
        prog=appConf.app_name,
        description='Migration migration engine for %(prog)s database')
    subparsers = parser.add_subparsers(title='Commands')
    parser_upgrade = subparsers.add_parser('upgrade', help='Upgrade database to the latest revision')
    parser_upgrade.set_defaults(cmd=db_migrate.upgrade, has_params=False)

    parser_downgrade = subparsers.add_parser('downgrade', help='Upgrade database to the needed revision')
    parser_downgrade.add_argument('params', nargs=1, type=str)
    parser_downgrade.set_defaults(cmd=db_migrate.downgrade, has_params=True)

    parser_info = subparsers.add_parser('info', help='Print current database path and version')
    parser_info.set_defaults(cmd=db_migrate.print_info, has_params=False)

    parser_commit = subparsers.add_parser('commit', help='Commit new database revision')
    parser_commit.add_argument('params', nargs=1, type=str)
    parser_commit.set_defaults(cmd=db_migrate.commit, has_params=True)

    args = parser.parse_args()

    try:
        if args.has_params:
            args.cmd(*args.params)
        else:
            args.cmd()
    except AttributeError:
        parser.print_help()
