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

from sqlalchemy import Column, Integer, UnicodeText
from sqlalchemy.orm import relationship
from . import BASE_MODEL


class User(BASE_MODEL):
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    username = Column(UnicodeText(40), unique=True)
    pwd_hash = Column(UnicodeText(80), unique=False)

    # currency code according to ISO 4217
    currency = Column(UnicodeText(3), nullable=False, default="USD", unique=False)

    budget_periods = relationship('BudgetPeriod', back_populates='owner')
