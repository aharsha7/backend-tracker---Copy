import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from app.routes.auth_routes import auth_bp
from app.routes.transaction_routes import transaction_bp
from app.routes.category_routes import category_bp
from app.extensions import db, migrate, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    JWTManager(app)
    CORS(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(category_bp)
    
    
    @app.route('/')
    def home():
        return "Budget Tracker Backend is Running 🚀"

    return app

if __name__ == "__main__":
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
    