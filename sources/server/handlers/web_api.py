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

from datetime import date
from tornado.web import HTTPError, authenticated

from db import CURRENCY_TYPES, PERIOD_TYPES
from .base import BaseHandler
from .errors import SignInError, SignUpError


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
        self.add_new_item(category=self.get_argument("category"),
                          date=date.today(),
                          title=self.get_argument("title"),
                          amount=self.get_argument("amount"),
                          currency="UAH")
        self.redirect(self.get_argument("next", "/"))


class AuthLoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # If there are no users, redirect to the account creation page.
        if not self.has_users():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    def post(self, *args, **kwargs):
        try:
            print(self.get_argument("email"))
            print(self.get_argument("password"))
            self.login_user(self.get_argument("email"), self.get_argument("password"))
            self.redirect(self.get_argument("next", "/"))
        except SignInError as e:
            self.render("login.html", error=e.description)


class AuthCreateHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("create_user.html", error=None)

    def post(self, *args, **kwargs):
        try:
            self.create_new_user(email=self.get_argument("email"),
                                 password=self.get_argument("password"),
                                 username=self.get_argument("username"))
            self.redirect("/settings")
        except SignUpError as e:
            self.render("create_user.html", error=e.description)


class AuthLogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_session_token()
        self.redirect(self.get_argument("next", "/"))


class SettingsHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render("budget_settings.html",
                    currency_arr=CURRENCY_TYPES,
                    periods=PERIOD_TYPES)

    @authenticated
    def put(self, *args, **kwargs):
        self.update_budget_plan(period=self.get_argument("period"),
                                currency=self.get_argument("currency"),
                                amount=self.get_argument("amount"))
        self.redirect(self.get_argument("next", "/"))


class SettingsPeriodHandler(BaseHandler):
    @authenticated
    def post(self, *args, **kwargs):
        self.update_budget_plan(period=self.get_argument("period"),
                                currency=self.get_argument("currency"),
                                amount=self.get_argument("amount"))
        self.redirect(self.get_argument("next", "/"))


class SettingsCategoryHandler(BaseHandler):
    @authenticated
    def post(self, *args, **kwargs):
        self.add_category(self.get_argument("category"))
        self.redirect(self.get_argument("next", "/"))


web_api_routes = [
    (r'/', MainHandler),
    (r'/budget', BudgetRequestHandler),
    (r"/auth/create", AuthCreateHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
    (r"/settings", SettingsHandler),
    (r"/settings/period", SettingsPeriodHandler),
    (r"/settings/category", SettingsCategoryHandler)
]
