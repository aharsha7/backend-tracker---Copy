from flask import request, jsonify
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not all([name, email, password, confirm_password]):
        return jsonify({"message": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    if User.query.filter_by(name=name).first():
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id, expires_delta=timedelta(days=1))

        response = {
            "token": access_token,
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }
        }

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while registering the user", "error": str(e)}), 500
    finally:
        db.session.remove()

    return jsonify(response), 201

def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Check if email and password are provided
    if not all([email, password]):
        return jsonify({"message": "Email and Password are required"}), 400

    # Retrieve the user by email
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and if the password matches
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
