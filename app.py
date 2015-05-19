#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, flash, redirect, render_template, url_for
from flask.ext.login import (
    LoginManager, login_required, login_user, logout_user
)
from sqlalchemy.orm.exc import NoResultFound
from authentication import User
from database import CommitSession, init_db, get_session
from forms import CreateInviteForm, RedeemForm
from model import Invitation
from utils import send_invitationmail

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.login_message_category = "error"
login_manager.init_app(app)
app.config.from_pyfile('config.py')


@login_manager.user_loader
def user_loader(user_id):
    # Dummy user creation, no real authentication
    return User("Logged van User")


@app.route('/')
def index():
    s = get_session()
    invs = s.query(Invitation).all()
    form = CreateInviteForm()
    return render_template("index.html", form=form, invs=invs)


@app.route('/invite/create', methods=['post'])
@login_required
def invite_create():
    form = CreateInviteForm()
    if form.validate_on_submit():
        with CommitSession() as cs:
            new_invitation = Invitation(
                creator=form.creator.data,
                created_for_mail=form.created_for_mail.data
            )
            cs.add(new_invitation)

        if send_invitationmail(
                new_invitation.created_for_mail,
                new_invitation.creator,
                new_invitation.token):
            flash("Invitation created and sent to {target}".format(
                target=new_invitation.created_for_mail), "success")
        else:
            flash("Invitation created, but could not be sent to {"
                  "target}!".format(target=new_invitation.created_for_mail),
                  "error")
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
                form.first_name.data+" "+form.last_name.data,
                i.created_for_mail))

            with CommitSession() as cs:
                # If the invitation was redeemed, set the flag
                i.redeem()
                cs.add(i)

            return redirect(url_for('index'))
        return render_template("invite/redeem.html", form=form, invite=i)
    except NoResultFound:
        flash("Token '{}' not valid!".format(invite_token), "error")
    return redirect(url_for('index'))


@app.route('/login')
def login():
    """Dummy function, does not yet authenticate against a valid backend
    """
    logged_in_user = User("Logged van User")
    login_user(logged_in_user)
    flash("You are now logged in as {}.".format(logged_in_user.name), "success")
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    flash("You were logged out.")
    return redirect(url_for('index'))


init_db()
s = get_session()
s.add(Invitation("Test Admin", "mail@awf.xy"))
s.commit()
app.run()
