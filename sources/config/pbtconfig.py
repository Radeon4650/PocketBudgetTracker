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
import shutil
import logging

from configparser import ConfigParser
from appdirs import AppDirs

logger = logging.getLogger('pbt.config')

CONFIG_NAME = 'pbtconfig.cfg'
CONFIG_DEFAULT = os.path.join(os.path.dirname(__file__), 'pbt_defaults.cfg')


class PbtConfig(object):
    def __init__(self):
        self.app_name = "pbtserver"
        self.author = "PBT Team"
        self.dirs = AppDirs(self.app_name, self.author)
        self.config_path = os.path.join(self.dirs.user_config_dir, CONFIG_NAME)
        self.config = ConfigParser()
        self._loaded = False

    @property
    def is_loaded(self):
        return self._loaded

    def load(self):
        self.config = ConfigParser()

        if not os.path.exists(self.dirs.user_config_dir):
            os.mkdir(self.dirs.user_config_dir)

        if not os.path.exists(self.config_path):
            shutil.copyfile(CONFIG_DEFAULT, self.config_path, follow_symlinks=True)

        try:
            self.config.read_file(open(self.config_path, encoding='utf-8'))
        except:
            logger.error("Couldn't read config from {}".format(self.config_path))
            self.config.read_file(open(CONFIG_DEFAULT, encoding='utf-8'))

        self._loaded = True

    def db_path(self):
        path = self.config["DB"]["path"]
        engine_type = self.config["DB"]["engine"]
        if engine_type == "sqlite":
            if str(path).startswith('/'):
                return "sqlite:///" + path
            else:
                return "sqlite:///" + os.path.join(self.dirs.user_config_dir, path)

        elif engine_type == "postgresql":
            return "postgresql://" + path
        return ""

    def host(self):
        return str(self.config["SERVER"]["ip"])

    def port(self):
        return int(self.config["SERVER"]["port"])
