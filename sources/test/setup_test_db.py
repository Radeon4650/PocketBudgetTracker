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

import os
import sys
import hashlib
from tornado_sqlalchemy import make_session_factory
from faker import Faker

src_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(src_root)
from db.models import BASE_MODEL, User, Budget

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
    categories = {'Food': ['Chicken breast', 'Bread', 'Salad', 'Milk', 'Chocolate', 'Sausage', 'Apples', 'Cake'],
                  'Home': ['Soap', 'Shampoo', 'Flower', 'Dinnerware', 'Trash bags'],
                  'Clothes': ['Jacket', 'Skirt', 'Sneakers', 'Hat', 'Blouse', 'Sweater'],
                  'Transport': ['Bus ticket', 'Gasoline 20 l', 'Car wash', 'Parking 8 h', 'Train ticket'],
                  'Entertainment': ['Restaurant', 'Cafe', 'Cinema', 'Gym membership'],
                  'Bills': ['Electricity', 'Cold water', 'Hot water', 'Internet', 'Heating', 'Mobile phone'],
                  'Other spendings': ['Gift for friend', 'Haircut', 'Manicure']}

    random_cat = fake.random_element(categories.keys())
    random_title = fake.random_element(categories[random_cat])
    Budget(
        owner=owner,
        category=random_cat,
        date=fake.date_this_year(),
        title=random_title,
        amount=fake.random_int(min=1, max=2000),
        currency="UAH")

users = [make_user() for _ in range(10)]

for new_user in users:
    budgets = [make_budget(new_user) for _ in range(fake.random_int(max=100))]
    session.add(new_user)
session.commit()