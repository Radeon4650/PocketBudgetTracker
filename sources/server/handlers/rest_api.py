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

import json
import logging

from tornado.web import Finish, authenticated
from dateutil import parser as date_parser

from .base import BaseHandler
from .errors import BaseApiError, BodyKeyError


logger = logging.getLogger('rest_api')


class RestBaseHandler(BaseHandler):
    def prepare(self):
        super(RestBaseHandler, self).prepare()
        self.set_header('Content-Type', 'application/json')

    def get_login_url(self):
        return "/api/auth/login"

    def get_json_data(self):
        try:
            data = json.loads(self.request.body.decode())
            return data
        except json.decoder.JSONDecodeError as e:
            logger.error("JSON parse error: %s" % e)
            self.set_status(400)
            raise Finish()

    def error(self, api_error):
        self.set_status(api_error.code)
        self.write({"error": api_error.__dict__})


class RestBudgetHandler(RestBaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        try:
            rest_dict = {}

            category = self.get_argument("category", None)
            if category:
                rest_dict["category"] = self.get_category(category).to_dict()
            else:
                rest_dict["categories"] = []
                for cat in self.current_user.categories:
                    rest_dict["categories"].append(cat.to_dict())

            self.set_status(200)
            self.write(rest_dict)
        except BaseApiError as e:
            self.error(e)

    @authenticated
    def post(self, *args, **kwargs):
        data_obj = self.get_json_data()
        try:
            self.add_new_item(category=data_obj["category"],
                              date=date_parser.parse(data_obj["date"]),
                              title=data_obj["title"],
                              amount=data_obj["amount"],
                              currency=data_obj["currency"])
            self.set_status(200)
        except (KeyError, ValueError):
            self.error(BodyKeyError())


class RestLoginHandler(RestBaseHandler):
    def post(self, *args, **kwargs):
        data_obj = self.get_json_data()
        try:
            self.login_user(data_obj["login"], data_obj["password"])
            self.set_status(200)
        except KeyError:
            self.error(BodyKeyError())

        except BaseApiError as e:
            self.error(e)


class RestCreateHandler(RestBaseHandler):
    def post(self, *args, **kwargs):
        data_obj = self.get_json_data()
        try:
            self.create_new_user(email=data_obj["email"],
                                 password=data_obj["password"],
                                 username=data_obj.get("username", None))
            self.set_status(200)
        except KeyError:
            err = BodyKeyError()
            self.set_status(err.code)
            self.write(err.__dict__)
        except BaseApiError as e:
            self.set_status(e.code)
            self.write(e.__dict__)


class RestLogoutHandler(RestBaseHandler):
    def get(self, *args, **kwargs):
        self.clear_session_token()
        self.set_status(200)


rest_api_routes = [
    (r"/api/auth/create", RestCreateHandler),
    (r"/api/auth/login", RestLoginHandler),
    (r"/api/auth/logout", RestLogoutHandler),
    (r"/api/budget", RestBudgetHandler)
]
