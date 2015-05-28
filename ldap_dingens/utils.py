# -*- coding: utf-8 -*-

import base64
import hashlib
import logging
import smtplib
import ssl

from email.utils import formatdate
from email.mime.text import MIMEText

import ldap3

import sqlalchemy.exc

logger = logging.getLogger(__name__)

from . import app
from . import database
from . import model


def send_invitationmail(target, invitation_creator, invitation_token):
    msg = """Hello {target},

{creator} invited you to create an account in FSFW LDAP!

Follow this link to redeem your invitation:
{baseurl}/{token}""".format(target=target,
                            creator=invitation_creator,
                            baseurl=app.config["INVITATION_REDEEM_BASEURL"],
                            token=invitation_token)

    mail = MIMEText(msg, _charset='utf-8')

    mail['From'] = app.config["INVITATION_SENDER"]
    mail['To'] = target
    mail['Subject'] = app.config["INVITATION_SUBJECT"]
    mail['Date'] = formatdate(localtime=True)

    ctx = ssl.create_default_context(cafile=app.config["MAIL_CAFILE"])
    ctx.verify_mode = ssl.CERT_REQUIRED

    try:
        # we have to pass the host + port to the constructor, for SSL to work
        # this might in fact be a bug in the python stdlib
        smtp = smtplib.SMTP(host=app.config["MAIL_SERVER"],
                            port=app.config["MAIL_PORT"])
        logger.debug("connected to SMTP server")
        smtp.starttls(context=ctx)
        logger.debug("starttls successful")
        if app.config["MAIL_USER"] and app.config["MAIL_PASSWORD"]:
            logger.debug("login needed, logging in")
            smtp.login(app.config["MAIL_USER"],
                       app.config["MAIL_PASSWORD"])
            logger.debug("logged in")
        smtp.sendmail(app.config["INVITATION_SENDER"], target, mail.as_string(0))
        logger.debug("sent mail")
        smtp.close()
        return True
    except IOError:
        logger.exception("failed to send mail")
        return False

def create_invitation(creator, created_for_mail, *, max_attempts=10):
    for i in range(max_attempts):
        try:
            with database.CommitSession() as cs:
                token = model.Invitation(creator, created_for_mail)
                cs.add(token)
            return token
        except sqlalchemy.exc.IntegrityError:
            logger.warn("failed to create token, %d attempts left",
                        (max_attempts-i)-1,
                        exc_info=True)


def transfer_ldap_user(ldap_conn, user_dn):
    if not ldap_conn.search(user_dn, "(objectClass=*)", ldap3.BASE,
                            attributes=["cn", "uid"]):
        # search failed, uhm
        return None

    displayname = ldap_conn.response[0]["attributes"]["cn"][0]
    loginname = ldap_conn.response[0]["attributes"]["uid"][0]

    with database.CommitSession() as cs:
        user = model.User(loginname, displayname)
        cs.add(user)
    return user
