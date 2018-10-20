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

import bcrypt
from sqlalchemy import Column, Integer, UnicodeText
from sqlalchemy.orm import relationship
from . import BASE_MODEL


class User(BASE_MODEL):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    token = Column(UnicodeText(150), unique=True, nullable=False)

    login = Column(UnicodeText(40), unique=True)
    pwd_hash = Column(UnicodeText(80), nullable=False, unique=False)
    username = Column(UnicodeText(40), nullable=False, unique=False)

    user_pic = Column(UnicodeText, nullable=True, unique=False)
    categories = relationship('Category', back_populates='owner')


def gen_salt():
    return str(bcrypt.gensalt().decode())


def password_hash(salt, password):
    return str(bcrypt.hashpw(password, salt).decode())
