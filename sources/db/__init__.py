# -*- coding: utf-8 -*-
"""
Copyright © 2018 PocketBudgetTracker. All rights reserved.
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
import logging

import sqlalchemy as sa
from tornado_sqlalchemy import make_session_factory
from .models import BASE_MODEL
from .models.user import User, Token
from .models.budget import Budget, Category

logger = logging.getLogger('server_db')


def make_db(db_uri):
    session_factory = make_session_factory(db_uri)
    fill_db_if_empty(session_factory.engine)
    return session_factory


def fill_db_if_empty(engine):
    table_names = sa.inspect(engine).get_table_names()
    is_empty = table_names == []
    if is_empty:
        logger.info('Database is empty, creating tables.')
        BASE_MODEL.metadata.create_all(engine)
