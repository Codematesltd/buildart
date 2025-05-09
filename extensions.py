from flask_login import LoginManager
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

login_manager = LoginManager()
login_manager.login_view = 'admin.login'

csrf = CSRFProtect()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()

def init_extensions(app):
    login_manager.init_app(app)
    csrf.init_app(app)
    talisman.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
