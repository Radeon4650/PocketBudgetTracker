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

from tornado.web import RequestHandler, HTTPError, authenticated
from tornado_sqlalchemy import SessionMixin

import bcrypt
import datetime

from db.models import User, Budget, Category, password_hash


class BaseHandler(SessionMixin, RequestHandler):
    def prepare(self):
        self.make_session()

    def get_current_user(self):
        user_token = self.get_secure_cookie("user_token")
        if user_token is None:
            return None

        return self.session.query(User).filter_by(token=user_token.decode()).first()

    def has_users(self):
        return self.session.query(User).count()


class MainHandler(BaseHandler):
    """
    Handler for the GET / request
    """

    def get(self):
        self.redirect("/budget")


class BudgetRequestHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("budget.html")

    @authenticated
    def post(self):
        category_name = self.get_argument("category")
        category = self.session.query(Category).filter_by(owner=self.current_user,
                                                          name=category_name).first()
        if not category:
            category = Category(name=category_name, owner=self.current_user)

        new_item = Budget(
            category=category,
            date=datetime.date.today(),
            title=self.get_argument("title"),
            amount=self.get_argument("amount"),
            currency="UAH")
        self.session.add(new_item)
        self.redirect(self.get_argument("next", "/"))


class AuthLoginHandler(BaseHandler):
    def get(self):
        # If there are no users, redirect to the account creation page.
        if not self.has_users():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    def post(self):
        email = self.get_argument("email")
        pwd_hash = password_hash(self.get_argument("email"), self.get_argument("password"))

        user = self.session.query(User).filter_by(login=email, pwd_hash=pwd_hash).first()
        if user is None:
            self.render("login.html", error="login failed")
        else:
            self.set_secure_cookie("user_token", user.token)
            self.redirect(self.get_argument("next", "/"))


class AuthCreateHandler(SessionMixin, RequestHandler):
    def get(self):
        self.render("create_user.html")

    def post(self):
        user_email = self.get_argument("email")
        user_passwd = self.get_argument("password")
        if not user_email or not user_passwd:
            raise HTTPError(400, "invalid input")

        user = self.session.query(User).filter_by(login=user_email).first()

        if user is not None:
            raise HTTPError(400, "email is already used")

        new_user = User(login=user_email,
                        token=str(bcrypt.gensalt().decode()),
                        username=self.get_argument("username", default=user_email),
                        pwd_hash=password_hash(user_email, user_passwd))
        self.session.add(new_user)

        self.set_secure_cookie("user_token", new_user.token)
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(RequestHandler):
    def get(self):
        self.clear_cookie("user_token")
        self.redirect(self.get_argument("next", "/"))


routes = [
    (r'/', MainHandler),
    (r'/budget', BudgetRequestHandler),
    (r"/auth/create", AuthCreateHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
]
