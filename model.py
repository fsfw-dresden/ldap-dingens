# -*- coding: utf-8 -*-
import base64
import random

from enum import Enum
from datetime import datetime, timedelta

from sqlalchemy import (
    Column, Integer, String, Boolean, UniqueConstraint,
    DateTime
)
from database import Base

try:
    from config import TOKEN_BYTES
except (ImportError, NameError):
    TOKEN_BYTES = 15

try:
    from config import TOKEN_LIFETIME
except (ImportError, NameError):
    TOKEN_LIFETIME = timedelta(days=7)

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
        self.expires = datetime.utcnow() + TOKEN_LIFETIME

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
        token_bits = TOKEN_BYTES * 8
        token_data = _rng.getrandbits(token_bits).to_bytes(
            TOKEN_BYTES, "little")
        return base64.urlsafe_b64encode(token_data).decode("ascii")
