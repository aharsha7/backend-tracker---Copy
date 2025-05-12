import pymysql
pymysql.install_as_MySQLdb()

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from app.config import Config
from app.routes.auth_routes import auth_bp
from app.routes.transaction_routes import transaction_bp
from app.routes.category_routes import category_bp
from app.extensions import db, migrate, jwt


def create_app():
    # Point to React build output folder
    app = Flask(__name__, static_folder='../frontend-budget/dist', static_url_path='')

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS for frontend dev and prod
    CORS(app, 
         resources={r"/*": {
             "origins": ["http://localhost:5173", "https://frontend-budget.vercel.app"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(category_bp)

    # Catch-all route to serve React app
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
