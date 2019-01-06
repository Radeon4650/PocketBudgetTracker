# -*- coding: utf-8 -*-
"""
Copyright © 2018 PocketBudgetTracker. All rights reserved.
Authors: Approximator (alex@nls.la)
         Andrey Shelest (khadsl1305@gmail.com)

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

from db import Migrate
from config import PbtConfig
from server import PBTServer

logger = logging.getLogger('pbt.main')
logging.basicConfig(
    format='%(asctime)s.%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level='INFO'
)

if __name__ == '__main__':
    pbt_config = PbtConfig()
    pbt_config.load()

    # upgrade database to the latest version
    migrate = Migrate(pbt_config.db_path())
    migrate.upgrade_head()

    pbt_server = PBTServer(pbt_config)
    pbt_server.run()
