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

import os
from datetime import date
from tornado.web import HTTPError, authenticated, StaticFileHandler

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
            self.login_user(self.get_argument("email"), self.get_argument("password"))
            self.redirect(self.get_argument("next", "/"))
        except SignInError as e:
            self.render("login.html", error=e.description)


class AuthCreateHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("create_user.html")

    def post(self, *args, **kwargs):
        try:
            self.create_new_user(email=self.get_argument("email"),
                                 password=self.get_argument("password"),
                                 username=self.get_argument("username"))
            self.redirect(self.get_argument("next", "/"))
        except SignUpError as e:
            raise HTTPError(e.code, e.description)


class AuthLogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_session_token()
        self.redirect(self.get_argument("next", "/"))


class NewUIHandler(StaticFileHandler):

    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.set_header('Expires', '0')

web_api_routes = [
    (r'/', MainHandler),
    (r'/ui/new/(.*)', NewUIHandler, {'path': os.path.join(os.path.dirname(__file__), '../../../pbt-ui/build')}),
    (r'/budget', BudgetRequestHandler),
    (r"/auth/create", AuthCreateHandler),
    (r"/auth/login", AuthLoginHandler),
    (r"/auth/logout", AuthLogoutHandler),
]
