from sqlalchemy import Column, Integer, String
from database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True)
    creator = Column(String)
    created_for_mail = Column(String)
