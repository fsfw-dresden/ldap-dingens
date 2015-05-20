# -*- coding: utf-8 -*-

import logging
import ssl

logger = logging.getLogger(__name__)

from email.utils import formatdate
from email.mime.text import MIMEText
import smtplib
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
        smtp.starttls(context=ctx)
        if MAIL_USER and MAIL_PASSWORD:
            print("logged in")
            smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.sendmail(INVITATION_SENDER, target, mail.as_string(0))
        smtp.close()
        return True
    except IOError:
        logger.exception("failed to send mail")
        return False


def create_user(first, last, mail):
    """LDAP connector
    """
    return True
