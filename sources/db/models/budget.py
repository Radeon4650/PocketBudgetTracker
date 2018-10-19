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

from sqlalchemy import Column, Integer, UnicodeText, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from . import BASE_MODEL


class Budget(BASE_MODEL):
    __tablename__ = 'budgets'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    category = relationship("Category", back_populates="budgets")
    category_id = Column(Integer, ForeignKey('categories.id'))

    date = Column(Date, nullable=False)
    title = Column(UnicodeText, nullable=False)
    amount = Column(Integer, nullable=False)

    # currency code according to ISO 4217
    currency = Column(UnicodeText(3), nullable=False, default="USD")

    def __repr__(self):
        return "{}: {} {} {} {}".format(self.id, self.title, str(self.date), self.amount, self.currency)


class Category(BASE_MODEL):
    __tablename__ = 'categories'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(UnicodeText, nullable=False)

    owner = relationship("User", back_populates="categories")
    owner_id = Column(Integer, ForeignKey('users.id'))

    budgets = relationship('Budget', back_populates='category')

    # unique constraint for group of owner_id and name
    __table_args__ = (UniqueConstraint('name', 'owner_id', name='_category_owner_uc'),)
