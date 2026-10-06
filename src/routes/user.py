from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from src.models.user import User, db

user_bp = Blueprint('user', __name__)


def _credentials(data):
    username = str(data.get('username', '')).strip()
    email = str(data.get('email', '')).strip().lower()
    password = data.get('password', '')
    if not username or not email or not password:
        return None
    return username, email, password


@user_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    credentials = _credentials(data)
    if not credentials:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    username, email, password = credentials
    if User.query.filter(or_(User.username == username, User.email == email)).first():
        return jsonify({'error': 'Username or email is already registered'}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'user': user.to_dict(),
        'access_token': create_access_token(identity=str(user.id)),
    }), 201


@user_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get('email', '')).strip().lower()
    password = data.get('password', '')
    user = User.query.filter_by(email=email).first()
    if not user or not password or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({
        'user': user.to_dict(),
        'access_token': create_access_token(identity=str(user.id)),
    })


@user_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())
