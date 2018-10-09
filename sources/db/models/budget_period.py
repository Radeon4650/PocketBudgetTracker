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

from sqlalchemy import Column, Integer, UnicodeText, ForeignKey
from sqlalchemy.orm import relationship
from . import BASE_MODEL


class BudgetPeriod(BASE_MODEL):
    __tablename__ = 'budget_periods'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    owner = relationship("User", back_populates="budget_periods")
    owner_id = Column(Integer, ForeignKey('users.id'))

    #TODO: add fields: limits
