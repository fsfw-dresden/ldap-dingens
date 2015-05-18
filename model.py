from random import choice
from sqlalchemy import Column, Integer, String
from database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    creator = Column(String, nullable=False)
    created_for_mail = Column(String, nullable=False)

    def __init__(self, creator, created_for_mail):
        self.token = Invitation.create_token()
        self.creator = creator
        self.created_for_mail = created_for_mail

    @staticmethod
    def create_token():
        symbols = "abcdefghjklmnopqrstuvwxyz"
        t = ""
        for i in range(8):
            t += symbols[choice(range(len(symbols)))]
        return t
