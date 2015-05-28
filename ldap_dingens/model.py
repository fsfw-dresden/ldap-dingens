# -*- coding: utf-8 -*-
import base64
import random

import flask.ext.login

from enum import Enum
from datetime import datetime, timedelta

from sqlalchemy import (
    Column, Integer, String, Boolean, UniqueConstraint,
    DateTime
)
from .database import Base, CommitSession

from . import app

_rng = random.SystemRandom()


class InvitationState(Enum):
    VALID = "Valid"
    REDEEMED = "Redeemed"
    EXPIRED = "Expired"


class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = (
        UniqueConstraint("token"),
    )

    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    redeemed = Column(Boolean)
    creator = Column(String, nullable=False)
    created_for_mail = Column(String, nullable=False)
    expires = Column(DateTime, nullable=False)

    def __init__(self, creator, created_for_mail):
        self.token = Invitation.create_token()
        self.redeemed = False
        self.creator = creator
        self.created_for_mail = created_for_mail
        self.expires = datetime.utcnow() + app.config["TOKEN_LIFETIME"]

    def redeem(self):
        self.redeemed = True

    def get_state(self):
        if self.redeemed:
            return InvitationState.REDEEMED
        elif datetime.utcnow() > self.expires:
            return InvitationState.EXPIRED
        else:
            return InvitationState.VALID

    @staticmethod
    def create_token():
        token_bytes = app.config["TOKEN_BYTES"]
        token_bits = token_bytes * 8
        token_data = _rng.getrandbits(token_bits).to_bytes(
            token_bytes, "little")
        return base64.b32encode(token_data).decode("ascii").lower()


class User(flask.ext.login.UserMixin, Base):
    __tablename__ = "ldap_session_users"

    auth_token = Column(String, primary_key=True)
    loginname = Column(String, nullable=False)
    displayname = Column(String, nullable=False)

    expires = Column(DateTime, nullable=False)

    def __init__(self, loginname, displayname):
        token_bytes = app.config["TOKEN_BYTES"]
        login_lifetime = app.config["LOGIN_LIFETIME"]
        self.auth_token = flask.ext.login.make_secure_token(
            loginname.encode("utf-8"),
            _rng.getrandbits(token_bytes*8).to_bytes(token_bytes, "little")
        )
        self.loginname = loginname
        self.displayname = displayname
        self.expires = datetime.utcnow() + login_lifetime

    def is_active(self):
        return datetime.utcnow() < self.expires

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.auth_token

    def get_auth_token(self):
        return self.auth_token

    def __str__(self):
        return "{} ({})".format(self.displayname, self.loginname)

    def __repr__(self):
        return "<User loginname={!r}>".format(self.loginname)


def clean_stale_users():
    """
    Purge expired sessions from the database.
    """
    with CommitSession() as cs:
        cs.query(User).filter(User.expires < datetime.utcnow()).delete()
