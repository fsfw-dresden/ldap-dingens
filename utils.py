# -*- coding: utf-8 -*-

from email.utils import formatdate
from email.mime.text import MIMEText
import smtplib
from config import (
    MAIL_SERVER, MAIL_PORT,
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

    try:
        smtp = smtplib.SMTP()
        smtp.connect(host=MAIL_SERVER, port=MAIL_PORT)
        smtp.sendmail(INVITATION_SENDER, target, mail.as_string(0))
        smtp.close()
        return True
    except IOError:
        return False
