#!/usr/bin/env python3

from flask import Flask, flash, redirect, render_template, url_for
from sqlalchemy.orm.exc import NoResultFound
from database import CommitSession, init_db, get_session
from forms import CreateInviteForm, RedeemForm
from model import Invitation

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def index():
    s = get_session()
    invs = s.query(Invitation).all()
    form = CreateInviteForm()
    return render_template("index.html", form=form, invs=invs)


@app.route('/invite/create', methods=['post'])
def invite_create():
    form = CreateInviteForm()
    if form.validate_on_submit():
        with CommitSession() as s:
            testinv = Invitation(
                creator=form.creator.data,
                created_for_mail=form.created_for_mail.data
            )
            s.add(testinv)
    return redirect(url_for('index'))


@app.route('/invite/redeem/<invite_token>', methods=['get', 'post'])
def invite_redeem(invite_token):
    form = RedeemForm()
    s = get_session()
    try:
        i = s.query(Invitation).filter_by(token=invite_token).one()
        if form.validate_on_submit():
            flash("Congratulations. A new LDAP user '{}' with email '{}' would "
                  "now be created.".format(
                form.first_name.data+" "+form.last_name.data, invite_token))
            return redirect(url_for('index'))
        return render_template("invite/redeem.html", form=form, invite=i)
    except NoResultFound:
        flash("Token '{}' not valid!".format(invite_token), "error")
    return redirect(url_for('index'))

init_db()
s = get_session()
s.add(Invitation("Test Admin", "mail@awf.xy"))
s.commit()
app.run()
