from datetime import timedelta

class DefaultConfiguration:
    DEBUG = False

    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USER = None
    MAIL_PASSWORD = None
    MAIL_CAFILE = None

    INVITATION_SUBJECT = "Invitation to join the FSFW!"

    TOKEN_BYTES = 5
    TOKEN_LIFETIME = timedelta(days=7)

    LOGIN_LIFETIME = timedelta(days=2)

    LDAP_SERVER = "localhost"
    LDAP_PORT = 389
