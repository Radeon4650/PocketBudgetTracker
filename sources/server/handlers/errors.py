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


class BaseApiError(Exception):

    def __init__(self, action="unknown_action", code=404, description="internal error"):
        super(BaseApiError, self).__init__()
        self.code = code
        self.action = action
        self.description = description


class SignUpError(BaseApiError):
    def __init__(self, description="user creation error"):
        super(SignUpError, self).__init__(action="new_user", code=400, description=description)


class SignInError(BaseApiError):
    def __init__(self, description="Incorrect username or password."):
        super(SignInError, self).__init__(action="login_user", code=401, description=description)


class BodyKeyError(BaseApiError):
    def __init__(self, description="invalid request data"):
        super().__init__(action="key_error", code=502, description=description)
