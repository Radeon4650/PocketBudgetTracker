# -*- coding: utf-8 -*-
"""
Database test
"""
# pylint: disable=all
import os
import hashlib

from pytest import fixture
from faker import Faker
from tornado_sqlalchemy import make_session_factory, SessionMixin
from sources.db.models import BASE_MODEL, User, Budget

fake = Faker('ru_RU')
DB_FILE = "/tmp/pbt_test.sqlite"


# =============== Helpers =====================
class AppHandler(SessionMixin):
    """
    This class mimics tornado's RequestHandler
    Needed only for convenient session_factory and SessionMixin usage
    """

    class App:

        def __init__(self):
            self._session_factory = make_session_factory('sqlite:///{}'.format(DB_FILE))
            self.settings = {'session_factory': self._session_factory}
            BASE_MODEL.metadata.create_all(self._session_factory.engine)

    def __init__(self):
        self.application = AppHandler.App()


@fixture(scope="module")  # will be called once for the entire test session
def session_factory():
    yield AppHandler()

    # this code bellow will be executed at the end of all tests
    print('\nRemove test DB: {}'.format(DB_FILE))
    # comment out next line if you want to peek into test database with some fake users ;)
    os.remove(DB_FILE)


@fixture
def fake_user_maker():

    class Maker:

        def make():
            return User(
                login=fake.user_name(),
                pwd_hash=hashlib.sha256(fake.password().encode()).hexdigest(),
                username=fake.name(),
                user_pic=fake.image_url())

    return Maker


# =============== Tests =====================


def test_users_add(session_factory, fake_user_maker):
    test_user = fake_user_maker.make()  # make some fake user
    test_user_login = test_user.login

    # add user to DB
    with session_factory.make_session() as session:  # this will automatically "commit" session if no exceptions thrown
        session.add(test_user)

    with session_factory.make_session() as session:
        # select newly added user
        users_from_db = session.query(User).filter(User.login == test_user_login).all()
        assert len(users_from_db) == 1
        assert users_from_db[0].login == test_user_login

        # add more check here
