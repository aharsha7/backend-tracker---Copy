from flask import Flask
from .config import Config
from .extensions import db, jwt, cors , migrate
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.transaction_routes import transaction_bp
    from app.routes.category_routes import category_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(category_bp, url_prefix='/api/categories')

    return app
