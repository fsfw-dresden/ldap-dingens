# -*- coding: utf-8 -*-
import base64
import random

from sqlalchemy import (
    Column, Integer, String, Boolean, UniqueConstraint
)
from database import Base

try:
    from config import TOKEN_BYTES
except (ImportError, NameError):
    TOKEN_BYTES = 15

_rng = random.SystemRandom()

class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = (
        UniqueConstraint("token"),
    )

    id = Column(Integer, primary_key=True)
    token = Column(String)
    redeemed = Column(Boolean)
    creator = Column(String, nullable=False)
    created_for_mail = Column(String, nullable=False)

    def __init__(self, creator, created_for_mail):
        self.token = Invitation.create_token()
        self.redeemed = False
        self.creator = creator
        self.created_for_mail = created_for_mail

    def redeem(self):
        self.redeemed = True

    def get_status(self):
        if self.redeemed:
            return "Redeemed"
        else:
            return "Not redeemed"

    @staticmethod
    def create_token():
        token_bits = TOKEN_BYTES * 8
        token_data = _rng.getrandbits(token_bits).to_bytes(
            TOKEN_BYTES, "little")
        return base64.urlsafe_b64encode(token_data).decode("ascii")
