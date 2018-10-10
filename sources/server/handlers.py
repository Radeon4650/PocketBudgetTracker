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

from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin

from db.models import User, Budget


class MainHandler(RequestHandler):
    """
    Handler for the GET / request
    """

    def get(self):
        self.write("<h3>Hello, Here is PocketBudgetTracker</h3>")


class BudgetRequestHandler(SessionMixin, RequestHandler):
    def get(self):
        with self.make_session() as session:
            current_user = session.query(User).first()
            items_str = ""
            for item in current_user.budgets:
                items_str += str(item)

            self.write("<h3>Hello '{}', there is {} items in you budget: </h3>"
                       "<br> {}".format(current_user.username, len(current_user.budgets), items_str))


routes = [
    (r'/', MainHandler),
    (r'/budget', BudgetRequestHandler),
]
