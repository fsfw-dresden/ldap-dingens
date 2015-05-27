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

    #: Host name of the LDAP server
    LDAP_SERVER = "localhost"

    #: str.format string to create a DN which refers to a user with a given
    #: loginname
    LDAP_USER_DN_FORMAT = "uid={loginname},ou=Account,dc=fsfw-dresden,dc=de"

    #: the DN to bind to for admin activity (create new users, change user
    #: info)
    LDAP_ADMIN_DN = "cn=AuthManager,ou=Management,dc=fsfw-dresden,dc=de"

    #: set this to the password for the LDAP_ADMIN_DN above
    LDAP_ADMIN_PASSWORD = ...
