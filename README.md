#FSFW LDAP-Dingens
Tool used to create, view and modify LDAP users.

As a registered user, you can create invitations which are sent to a not yet 
registered user. The receiver can then redeem the invitation token to provide
more user profile data and create the account.

## Setup
Make a virtualenv and run `pip install -r requirements.txt`. This should 
install all needed libraries.

If you run the program in `DEBUG = True` mode, it needs to be able to create 
the database at `/tmp/fsfw-inviter.db`. If debug is off, the database runs in
 memory and is system independent.