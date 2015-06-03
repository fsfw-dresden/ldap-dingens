import ldap3
import sys

from ldap_dingens import app, get_session, init_db, Invitation
from ldap_dingens.database import init_engine
from ldap_dingens.ldap import init_ldap

sys.path.insert(0, app.instance_path)
try:
    import config
finally:
    sys.path.remove(app.instance_path)

app.config.from_object(config.Configuration)

init_ldap()
init_engine()
init_db()
if app.DEBUG:
    # only create test invitation in debug mode
    session = get_session()
    session.add(Invitation("Test Admin", "mail@awf.xy"))
    session.commit()
app.run()
