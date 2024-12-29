from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from config import Config
from hashlib import sha256
from urllib.parse import urlencode

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()
bootstrap = Bootstrap5()
login_manager = LoginManager()
def gravatar_url(email, size=100, rating='g', default='retro', force_default=False):
    hash_value = sha256(email.lower().encode('utf-8')).hexdigest()
    query_params = urlencode({'d': default, 's': str(size), 'r': rating, 'f': force_default})
    return f"https://www.gravatar.com/avatar/{hash_value}?{query_params}"

@login_manager.user_loader
def load_user(user_id):
    from api.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    app.jinja_env.filters['gravatar'] = gravatar_url    
    login_manager.login_view = "routes.login"
    # ckeditor.config(default:{"versionCheck"=False})

    # Register routes blueprints
    from api.routes import routes_bp
    app.register_blueprint(routes_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
