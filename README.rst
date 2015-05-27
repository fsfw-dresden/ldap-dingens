FSFW LDAP-Dingens
#################

Tool used to create, view and modify LDAP users.

As a registered user, you can create invitations which are sent to a not yet
registered user. The receiver can then redeem the invitation token to provide
more user profile data and create the account.

Setup
=====

Make a virtualenv and run `python3 setup.py install`. This should install all
needed libraries, as well as the tool itself. You still need an entry point
such as the demo entry point included in the source (``app.py``) to load the
configuration and glue the parts together.

If you run the program in `DEBUG = True` mode, it needs to be able to create
the database at `/tmp/fsfw-inviter.db`. If debug is off, the database runs in
memory and is system independent.
