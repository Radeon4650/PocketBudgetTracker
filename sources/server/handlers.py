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
from datetime import datetime, date, timedelta

from tornado.web import RequestHandler, HTTPError, authenticated
from tornado_sqlalchemy import SessionMixin

from db import User, Budget, Category, Token

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
        if not session_token:
            return None

        if session_token.expiring_date < datetime.now():
            self.session.remove(session_token)
            return None
        return session_token

    def get_current_user(self):
        token = self.get_session_token()
        if token:
            return token.owner
        return None

    def has_users(self):
        return self.session.query(User).count()

    def password_hash(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def activate_session_token(self, user):
        session_token = Token(owner=user,
                              data=bcrypt.gensalt(30).decode(),
                              expiring_date=datetime.today() + timedelta(days=2))
        self.set_secure_cookie(TOKEN_COOKIE_NAME, session_token.data)
        self.session.add(session_token)


class MainHandler(BaseHandler):
    """
    Handler for the GET / request
    """

    def get(self, *args, **kwargs):
        self.redirect("/budget")


class BudgetRequestHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render("budget.html")

    @authenticated
    def post(self, *args, **kwargs):
        category_name = self.get_argument("category")
        category = self.session.query(Category).filter_by(owner=self.current_user,
                                                          name=category_name).first()
        if not category:
            category = Category(name=category_name, owner=self.current_user)

        new_item = Budget(
            category=category,
            date=date.today(),
            title=self.get_argument("title"),
            amount=self.get_argument("amount"),
            currency="UAH")
        self.session.add(new_item)
        self.redirect(self.get_argument("next", "/"))


class AuthLoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # If there are no users, redirect to the account creation page.
        if not self.has_users():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    def post(self, *args, **kwargs):
        email = self.get_argument("email")
        raw_password = self.get_argument("password")

        if not email or not raw_password:
            self.render("login.html", error="empty credential")

        user = self.session.query(User).filter_by(login=email).first()
        if user is None:
            self.render("login.html", error="login failed")

        if bcrypt.checkpw(raw_password.encode(), user.pwd_hash.encode()):
            self.activate_session_token(user)
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="login failed")


class AuthCreateHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("create_user.html")

    def post(self, *args, **kwargs):
        user_email = self.get_argument("email")
        user_passwd = self.get_argument("password")

        if not user_email or not user_passwd:
            raise HTTPError(400, "invalid input")

        user = self.session.query(User).filter_by(login=user_email).first()

        if user is not None:
            raise HTTPError(400, "email is already used")

        new_user = User(login=user_email,
                        username=self.get_argument("username", default=user_email),
                        pwd_hash=self.password_hash(user_passwd))

        self.activate_session_token(new_user)
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        active_token = self.get_session_token()
        self.session.remove(active_token)
        self.clear_cookie(TOKEN_COOKIE_NAME)
        self.redirect(self.get_argument("next", "/"))


routes = [
    (r'/', MainHandler),
    (r'/budget', BudgetRequestHandler),
    (r"/auth/create", AuthCreateHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
]
