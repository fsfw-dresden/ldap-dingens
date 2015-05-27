import ldap3
import sys

from ldap_dingens import app, get_session, init_db, Invitation
from ldap_dingens.database import init_engine

sys.path.insert(0, app.instance_path)
try:
    import config
finally:
    sys.path.remove(app.instance_path)

app.config.from_object(config.Configuration)

# XXX: this will be fixed later...
import ldap_dingens
ldap_dingens.ldap_server = ldap3.Server(app.config["LDAP_SERVER"])

init_engine()
init_db()
session = get_session()
session.add(Invitation("Test Admin", "mail@awf.xy"))
session.commit()
app.run()
