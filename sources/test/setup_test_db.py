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

import hashlib
from tornado_sqlalchemy import make_session_factory
from sources.db.models import BASE_MODEL, User, Budget
from faker import Faker

fake = Faker('ru_RU')
session_factory = make_session_factory('sqlite:////tmp/pbt_test.db')
BASE_MODEL.metadata.create_all(session_factory.engine)

session = session_factory.make_session()


def make_user():
    return User(
        login=fake.user_name(),
        pwd_hash=hashlib.sha256(fake.password().encode()).hexdigest(),
        username=fake.name(),
        user_pic=fake.image_url())


def make_budget(owner):
    Budget(
        owner=owner,
        category=fake.word(),
        date=fake.date_this_year(),
        title=fake.catch_phrase(),
        amount=fake.random_int(),
        currency=fake.currency_code())

users = [make_user() for _ in range(10)]

for new_user in users:
    budgets = [make_budget(new_user) for _ in range(fake.random_int(max=100))]
    session.add(new_user)
session.commit()
