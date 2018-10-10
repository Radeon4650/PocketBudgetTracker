# -*- coding: utf-8 -*-
"""
Copyright © 2018 PocketBudgetTracker. All rights reserverd.
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

logger = logging.getLogger('dev_script')
logging.basicConfig(
    format='%(asctime)s.%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level='INFO')

from server import PBTServer

if __name__ == '__main__':

    # TODO: implement loading settings from local config file
    pbt_server = PBTServer(
        ip='127.0.0.1',
        port=8788,
        db_path='sqlite:////tmp/pbt_test.db'
    )
    pbt_server.run()