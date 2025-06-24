"""Simple token-based auth for demonstration."""

import uuid
from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash

from .database import SessionLocal
from . import models

# In-memory token store {token: user_id}
auth_tokens = {}


def generate_token(user_id):
    token = str(uuid.uuid4())
    auth_tokens[token] = user_id
    return token


def get_user_from_token(token):
    user_id = auth_tokens.get(token)
    if not user_id:
        return None
    session = SessionLocal()
    user = session.get(models.User, user_id)
    session.close()
    return user


def token_required(role=None):
    """Decorator to protect endpoints with token auth and optional role."""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Auth token required"}), 401
            user = get_user_from_token(token)
            if not user:
                return jsonify({"error": "Invalid token"}), 401
            if role and user.role != role:
                return jsonify({"error": "Forbidden"}), 403
            request.user = user
            return f(*args, **kwargs)

        return wrapper

    return decorator


def login(email, password):
    session = SessionLocal()
    user = session.query(models.User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        session.close()
        return None
    token = generate_token(user.user_id)
    session.close()
    return token
