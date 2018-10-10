# -*- coding: utf-8 -*-
"""
Copyright © 2018 PocketBudgetTracker. All rights reserverd.
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

import datetime
from tornado_sqlalchemy import make_session_factory
from db.models import BASE_MODEL, User, Budget


session_factory = make_session_factory('sqlite:////tmp/pbt_test.db')
BASE_MODEL.metadata.create_all(session_factory.engine)

session = session_factory.make_session()

new_user = User(login='test_user', pwd_hash='test_pwd', username='test', user_pic='/some/pic')
new_budget = Budget(owner=new_user, category='category', date=datetime.date.today(),
                    title='something', amount=10, currency='UAH')

session.add(new_user)
session.commit()

