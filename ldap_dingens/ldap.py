import base64
import hashlib

import ldap3

from . import app
from . import model


def init_ldap():
    """
    Initialize the LDAP subsystem. This must be called once after the app
    configuration has been read.
    """
    global server

    server = ldap3.Server(app.config["LDAP_SERVER"])


def get_admin_conn():
    """
    Return a bound :class:`ldap3.Connection` instance which has write
    permissions on the dn in which the user accounts reside.
    """
    conn = get_conn(user=app.config["LDAP_ADMIN_DN"],
                    password=app.config["LDAP_ADMIN_PASSWORD"],
                    raise_exceptions=True)
    conn.bind()
    return conn


def get_conn(**kwargs):
    """
    Return an unbound :class:`ldap3.Connection` which talks to the configured
    LDAP server.

    The *kwargs* are passed to the constructor of :class:`ldap3.Connection` and
    can be used to set *user*, *password* and other useful arguments.
    """
    global server
    return ldap3.Connection(server, **kwargs)


def ssha_password(password):
    """
    Apply the SSHA password hashing scheme to the given *password*. *password*
    must be a :class:`bytes` object, containing the utf-8 encoded password.

    Return a :class:`bytes` object containing ``ascii``-compatible data which
    can be used as LDAP value, e.g. after armoring it once more using base64 or
    decoding it to unicode from ``ascii``.
    """
    SALT_BYTES = 15

    sha1 = hashlib.sha1()
    salt = model._rng.getrandbits(SALT_BYTES*8).to_bytes(SALT_BYTES, "little")
    sha1.update(password)
    sha1.update(salt)

    digest = sha1.digest()
    passwd = b"{SSHA}" + base64.b64encode(digest + salt)
    return passwd


def create_user(loginname, displayname, mail, password):
    """
    Create a new user in the LDAP storage.

    *loginname* must be a unique, valid user id. It is generally safe to pass
    lower-case ascii letters here. The *loginname* of an account cannot be
    changed.

    *displayname* is the name which is shown to other users. This can be
    changed in the future.

    *mail* is a valid mail address of the user.

    *password* is the initial plain text password for the user.
    """

    conn = get_admin_conn()
    try:
        conn.add(
            app.config["LDAP_USER_DN_FORMAT"].format(loginname=loginname),
            ["inetOrgPerson"],
            {
                "uid": [loginname],
                "cn": [displayname],
                "sn": ["XXX"],
                "givenName": ["XXX"],
                "mail": [mail],
                "userpassword": [ssha_password(password.encode("utf-8"))]
            })
    finally:
        conn.unbind()


def change_password(bound_conn, new_password):
    """
    Change the password of an LDAP user. *bound_conn* must be a
    :class:`ldap3.Connection` which is bound to the DN identifying the user
    whose password should be changed.

    *new_password* must be the new plain text password.
    """
    bound_conn.modify(
        bound_conn.user,
        {
            "userpassword": (ldap3.MODIFY_REPLACE,
                             [ssha_password(new_password.encode("utf-8"))])
        })
