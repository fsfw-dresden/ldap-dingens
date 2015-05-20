# -*- coding: utf-8 -*-

import logging
import smtplib
import ssl

from email.utils import formatdate
from email.mime.text import MIMEText

import sqlalchemy.exc

logger = logging.getLogger(__name__)

import database
import model

from config import (
    MAIL_SERVER, MAIL_PORT, MAIL_USER, MAIL_PASSWORD, MAIL_CAFILE,
    INVITATION_SENDER, INVITATION_SUBJECT, INVITATION_REDEEM_BASEURL
)


def send_invitationmail(target, invitation_creator, invitation_token):
    msg = """Hello {target},

{creator} invited you to create an account in FSFW LDAP!

Follow this link to redeem your invitation:
{baseurl}/{token}""".format(target=target,
                            creator=invitation_creator,
                            baseurl=INVITATION_REDEEM_BASEURL,
                            token=invitation_token)

    mail = MIMEText(msg, _charset='utf-8')

    mail['From'] = INVITATION_SENDER
    mail['To'] = target
    mail['Subject'] = INVITATION_SUBJECT
    mail['Date'] = formatdate(localtime=True)

    ctx = ssl.create_default_context(cafile=MAIL_CAFILE)
    ctx.verify_mode = ssl.CERT_REQUIRED

    try:
        # we have to pass the host + port to the constructor, for SSL to work
        # this might in fact be a bug in the python stdlib
        smtp = smtplib.SMTP(host=MAIL_SERVER, port=MAIL_PORT)
        logger.debug("connected to SMTP server")
        smtp.starttls(context=ctx)
        logger.debug("starttls successful")
        if MAIL_USER and MAIL_PASSWORD:
            logger.debug("login needed, logging in")
            smtp.login(MAIL_USER, MAIL_PASSWORD)
            logger.debug("logged in")
        smtp.sendmail(INVITATION_SENDER, target, mail.as_string(0))
        logger.debug("sent mail")
        smtp.close()
        return True
    except IOError:
        logger.exception("failed to send mail")
        return False


def create_user(first, last, mail, password):
    """LDAP connector
    """
    return True


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
