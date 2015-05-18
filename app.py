#!/usr/bin/env python3

from flask import Flask, redirect, render_template, url_for
from database import CommitSession, init_db, get_session
from model import Invitation

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def index():
    s = get_session()
    invs = s.query(Invitation).all()
    return render_template("index.html", invs=invs)


@app.route('/invite/create')
def invite_create():
    with CommitSession() as s:
        testinv = Invitation(creator="Dominik", created_for_mail="test@abc.xy")
        s.add(testinv)
    return render_template("invite/create.html")


@app.route('/invite/redeem/<string:invite_id>')
def invite_redeem(invite_id):
    if not invite_id:
        return redirect(url_for('index'))
    return render_template("invite/redeem.html", invite_id=invite_id)

init_db()
app.run()
