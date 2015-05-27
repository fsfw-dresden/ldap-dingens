# -*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from . import app


class CommitSession(object):
    """Get a commit session by using 'with' without calling commit()
    every time.
    """
    def __init__(self):
        self.session = get_session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()


def init_engine():
    """Because in-memory databases don't work together with multiple threads
    like flask uses in debug mode, switch to a file based database. Means,
    if you disable debug mode, the engine creates the database only in memory.
    """
    global engine

    if app.config["DEBUG"]:
        db_uri = '/tmp/fsfw-inviter.db'
        if os.path.exists(db_uri):
            print("Removing existing database file at {}.".format(db_uri))
            os.remove(db_uri)
        engine = create_engine('sqlite:///{}'.format(db_uri), echo=False)
    else:
        engine = create_engine('sqlite:///:memory:', echo=False)


def init_db():
    """Create all tables based on the models in model.py
    """
    Base.metadata.create_all(engine)


def get_session():
    global session
    if not session:
        s = scoped_session(sessionmaker(bind=engine))
        session = s()
    return session

Base = declarative_base()
session = None
