from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.config import Config


db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, origins="*")

    from app.routes import (
        health_bp,
        locations_bp,
        categories_bp,
        schemes_bp,
        analysis_bp,
        financial_bp,
        ai_bp,
        auth_bp,
        admin_bp,
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(schemes_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(financial_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        # Import models after the extension exists so SQLAlchemy can register
        # every table before creating the local development database.
        from app import models as _models  # noqa: F401

        db.create_all()

    return app