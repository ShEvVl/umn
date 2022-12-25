from flask import Flask
from app.models import db, migrate
from config import Config
from app.routes import main


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(main)
    with app.app_context():
        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)
    return app
