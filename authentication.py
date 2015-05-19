# -*- coding: utf-8 -*-

from flask.ext.login import UserMixin


class User(UserMixin):
    """User class to use with authentication via flask-login
    """

    def __init__(self, name):
        self.id = 1
        self.name = name

    def __repr__(self):
        return "<User {} named '{}'>".format(self.id, self.name)