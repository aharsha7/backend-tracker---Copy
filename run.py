import pymysql
pymysql.install_as_MySQLdb()
import os
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_cors import CORS
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
    CORS(app, supports_credentials=True, origins=["https://frontend-budget.vercel.app/"])
    
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
        
    # Change app.run() to listen on 0.0.0.0 with dynamic port for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    