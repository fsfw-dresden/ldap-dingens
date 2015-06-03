# -*- coding: utf-8 -*-

# The config must be placed into the instance_root of the application. The path
# of the instance_root defaults to the ``instance`` folder next to the package
# (which is not included in the default installation).

from datetime import timedelta

from ldap_dingens.default_config import DefaultConfiguration

class Configuration(DefaultConfiguration):
    # This class shows the defaults commented out. Override or pin to your
    # liking. Also, anything which uses `...` as a value must be set by
    # yourself and not commented out.

    #: Enable or disable debugging
    # DEBUG = False

    #: Host at which to reach your mail server (MTA)
    # MAIL_SERVER = "localhost"

    #: Hostname to use for SSL verification purposes
    # MAIL_SERVER_HOSTNAME = MAIL_SERVER

    #: Port at which your MTA listens
    # MAIL_PORT = 25

    #: User name to authenticate with the mail server. Set to None to disable
    #: authentication
    # MAIL_USER = None

    #: Password to use to authenticate with the mail server. Set to None to
    #: disable authentication.
    # MAIL_PASSWORD = None

    #: Certificate Authority file to verify the mail servers SSL server
    #: certificate. Use this only if the mail servers SSL certificate is not
    #: accepted by the local CA store. Set to None to disable this
    #: functionality.
    # MAIL_CAFILE = None

    #: Subject to use for invitation emails
    # INVITATION_SUBJECT = "Invitation to join the FSFW!"

    #: From address to use for invitation emails
    INVITATION_SENDER = ...

    #: URL format for invitation URLs. The invitation code is appended as a
    #: query string
    INVITATION_REDEEM_BASEURL = ...

    #: Number of random bytes for invitation tokens. Use multiples of 5 to
    #: achieve nice looking codes.
    # TOKEN_BYTES = 5

    #: Lifetime of invitation tokens
    # TOKEN_LIFETIME = timedelta(days=7)

    #: Lifetime of logins. If the login is older than that, the user is logged
    #: out automatically. Stale LDAP data lives at most that long.
    # LOGIN_LIFETIME = timedelta(days=2)

    #: Host name of the LDAP server
    # LDAP_SERVER = "localhost"

    #: str.format string to create a DN which refers to a user with a given
    #: loginname. The loginname is passed as a keyword argument `loginname` to
    #: the format method.
    LDAP_USER_DN_FORMAT = ...

    #: the DN to bind to for admin activity (create new users, change user
    #: info)
    LDAP_ADMIN_DN = ...

    #: set this to the password for the LDAP_ADMIN_DN above
    LDAP_ADMIN_PASSWORD = ...
