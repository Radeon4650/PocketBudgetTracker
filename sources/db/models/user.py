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

from sqlalchemy import Column, Integer, UnicodeText, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from . import BASE_MODEL, PERIOD_TYPES, CURRENCY_TYPES


class User(BASE_MODEL):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    login = Column(UnicodeText(40), unique=True)
    pwd_hash = Column(UnicodeText(80), nullable=False, unique=False)
    username = Column(UnicodeText(40), nullable=False, unique=False)

    # Budget configuration
    # currency code according to ISO 4217
    currency = Column(UnicodeText(3), nullable=False, default=CURRENCY_TYPES[0])
    period_type = Column(UnicodeText(10), nullable=False, default=PERIOD_TYPES[0])
    period_amount = Column(Integer, nullable=False, default=100)

    user_pic = Column(UnicodeText, nullable=True, unique=False)
    categories = relationship('Category', back_populates='owner')
    tokens = relationship('Token', back_populates='owner')


class Token(BASE_MODEL):
    __tablename__ = "tokens"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    data = Column(UnicodeText(80), unique=True, nullable=False)

    owner = relationship("User", back_populates="tokens")
    owner_id = Column(Integer, ForeignKey('users.id'))

    expiring_date = Column(DateTime(), nullable=False)
    expired = Column(Boolean, default=False, nullable=False)
