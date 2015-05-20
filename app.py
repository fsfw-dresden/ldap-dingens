#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FSFW LDAP-Dingens
Copyright (C) 2015 Dominik Pataky <mail@netdecorator.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

This licence text applies to all other files in this repository as well.

The source code which is used to run the application at fsfw-dresden.de is
available at https://github.com/fsfw-dresden/ldap-dingens
"""

from flask import Flask, flash, redirect, render_template, url_for
from flask.ext.login import (
    LoginManager, login_required, login_user, logout_user
)
from sqlalchemy.orm.exc import NoResultFound
from authentication import User
from database import CommitSession, init_db, get_session
from forms import CreateInviteForm, RedeemForm
from model import Invitation
from utils import create_user, send_invitationmail

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
    """Invitation creation form for logged in (=existing) users.
    """
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
    """GET and POST handler for a not yet registered user who wants to redeem
    an invitation token.
    """
    form = RedeemForm()
    s = get_session()

    try:
        invitation = s.query(Invitation).filter_by(token=invite_token).one()
    except NoResultFound:
        # No invitation with the supplied token found
        flash("Token '{}' not valid!".format(invite_token), "error")
        return redirect(url_for('index'))

    if invitation.redeemed:
        # Invitation is already redeemed, no second usage allowed
        flash("Invitation with token '{}' is already redeemed!".format(
            invitation.token), "error")
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # Receive POST data supplied via the form
        fn = form.first_name.data
        ln = form.last_name.data
        ma = invitation.created_for_mail
        pwd = form.password.data

        if create_user(fn, ln, ma, pwd):
            flash("New LDAP user '{}' with email '{}' was created.".format(
                fn + " " + ln, ma), "success")

            with CommitSession() as cs:
                # If the invitation was redeemed, set the flag
                invitation.redeem()
                cs.add(invitation)
        else:
            # TODO: LDAP exception handling
            flash("New user could not be created!", "error")

        return redirect(url_for('index'))

    # If the invitation was found, was not yet redeemed and its a GET, send form
    return render_template("invite/redeem.html", form=form, invite=invitation)


@app.route('/login')
def login():
    """Dummy function, does not yet authenticate against a valid backend
    """
    logged_in_user = User("Logged van User")
    login_user(logged_in_user)
    flash("You are now logged in as {}.".format(logged_in_user.name))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    flash("You were logged out.")
    return redirect(url_for('index'))


init_db()
session = get_session()
session.add(Invitation("Test Admin", "mail@awf.xy"))
session.commit()
app.run()
