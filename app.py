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

import ldap3

from flask import Flask, flash, redirect, render_template, url_for
from flask.ext.login import (
    LoginManager, login_required, login_user, logout_user
)
from sqlalchemy.orm.exc import NoResultFound
from database import CommitSession, init_db, get_session
from forms import CreateInviteForm, RedeemForm, LoginForm
from model import Invitation, InvitationState, User
from utils import (
    create_user, send_invitationmail, create_invitation,
    transfer_ldap_user
)

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.login_message_category = "error"
login_manager.init_app(app)
app.config.from_pyfile('config.py')

@login_manager.user_loader
def user_loader(user_id):
    return get_session().query(User).get(user_id)


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
        new_invitation = create_invitation(
            form.creator.data,
            form.created_for_mail.data)

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

    if invitation.get_state() != InvitationState.VALID:
        # Invitation is already redeemed or expired
        flash("Token '{}' not valid!".format(
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


@app.route('/login', methods=['get', 'post'])
def login():
    """Dummy function, does not yet authenticate against a valid backend
    """

    from config import LDAP_USER_DN_FORMAT

    form = LoginForm()

    if form.validate_on_submit():
        # we rely on the validation of the loginname in the form to be safe
        # from producing an invalid DN
        user_dn = LDAP_USER_DN_FORMAT.format(loginname=form.loginname.data)
        try:
            conn = ldap3.Connection(ldap_server,
                                    user=user_dn,
                                    password=form.password.data,
                                    raise_exceptions=True)
            conn.bind()
        except ldap3.LDAPInvalidCredentialsResult:
            form.password.errors.append("Login name or password is not valid")
            return render_template("login.html", form=form)

        user = transfer_ldap_user(conn, user_dn)
        conn.unbind()

        login_user(user)
        flash("You are now logged in as {} ({}).".format(
            user.displayname,
            user.loginname))

        return redirect(url_for('index'))

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You were logged out.")
    return redirect(url_for('index'))


from config import LDAP_SERVER

ldap_server = ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL)

init_db()
session = get_session()
session.add(Invitation("Test Admin", "mail@awf.xy"))
session.commit()
app.run()
