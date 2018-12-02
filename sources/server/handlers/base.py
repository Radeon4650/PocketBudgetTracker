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

from datetime import datetime, timedelta
import bcrypt

from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin

from db import User, Budget, Category, Token, PERIOD_TYPES, CURRENCY_TYPES
from .errors import SignUpError, SignInError, BodyKeyError

TOKEN_COOKIE_NAME = "user_token"


class BaseHandler(SessionMixin, RequestHandler):
    def data_received(self, chunk):
        pass

    def prepare(self):
        self.make_session()

    def get_session_token(self):
        user_token = self.get_secure_cookie(TOKEN_COOKIE_NAME)
        if not user_token:
            return None

        session_token = self.session.query(Token).filter_by(data=user_token.decode()).first()
        return session_token

    def get_current_user(self):
        token = self.get_session_token()
        if not token:
            return None

        if token.expiring_date < datetime.now():
            self.clear_session_token()
            return None

        return token.owner

    def has_users(self):
        return self.session.query(User).count()

    def activate_session_token(self, user):
        session_token = Token(owner=user,
                              data=bcrypt.gensalt(30).decode(),
                              expiring_date=datetime.today() + timedelta(days=2))
        self.set_secure_cookie(TOKEN_COOKIE_NAME, session_token.data)
        self.session.add(session_token)

    def clear_session_token(self):
        active_token = self.get_session_token()
        if active_token:
            self.session.delete(active_token)
        self.clear_cookie(TOKEN_COOKIE_NAME)

    def create_new_user(self, email, password, **params):
        if not email or not password:
            raise SignUpError("invalid input")

        user = self.session.query(User).filter_by(login=email).first()

        if user is not None:
            raise SignUpError("email is already used")

        new_user = User(login=email,
                        username=params.get("username", email),
                        pwd_hash=password_hash(password))

        self.activate_session_token(new_user)

    def login_user(self, email, password):
        if not email or not password:
            raise SignInError(description="empty credentials")

        user = self.session.query(User).filter_by(login=email).first()
        if user is None:
            raise SignInError()

        if bcrypt.checkpw(password.encode(), user.pwd_hash.encode()):
            self.activate_session_token(user)
        else:
            raise SignInError()

    def add_new_item(self, category_id, **arguments):
        category = self.session.query(Category).filter_by(id=category_id,
                                                          owner=self.current_user).first()
        if not category:
            raise BodyKeyError('invalid category %s' % category)

        new_item = Budget(
            category=category,
            date=arguments["date"],
            title=arguments["title"],
            amount=arguments["amount"],
            currency=arguments["currency"])
        self.session.add(new_item)

    def add_category(self, category_name):
        category = self.session.query(Category).filter_by(owner=self.current_user,
                                                          name=category_name).first()
        if not category:
            category = Category(name=category_name, owner=self.current_user)
            self.session.add(category)

    def get_category(self, name):
        category = self.session.query(Category).filter_by(name=name, owner=self.current_user).first()
        if not category:
            raise BodyKeyError('invalid category %s' % category)
        return category

    def delete_category(self, category_id, delete_items=False):
        category = self.session.query(Category).filter_by(owner=self.current_user,
                                                          id=category_id).first()
        if not category:
            raise BodyKeyError("category %s doesn't exist" % category_id)
        else:
            if delete_items is not None:
                for item in category.budgets:
                    self.session.delete(item)
            self.session.delete(category)

    def update_budget_plan(self, period, currency, amount):
        if period in PERIOD_TYPES:
            self.current_user.period_type = period

        if currency in CURRENCY_TYPES:
            self.current_user.currency = currency

        self.current_user.period_amount = amount


def password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
