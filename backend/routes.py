"""Flask routes exposing basic CRUD operations."""

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from .database import SessionLocal
from . import models
from . import auth
import uuid

api_bp = Blueprint("api", __name__)


@api_bp.route("/organizations", methods=["POST"])
def create_organization():
    """Create a new organization record.

    WHY: Sample endpoint to demonstrate DB interaction.
    WHAT: closes #init-setup
    HOW: Extend by adding authentication. Roll back by dropping table.
    """
    data = request.get_json() or {}
    org = models.Organization(
        organization_id=data.get("organization_id") or str(uuid.uuid4()),
        name=data.get("name"),
        type=data.get("type"),
        address=data.get("address"),
    )
    session: Session = SessionLocal()
    session.add(org)
    session.commit()
    return jsonify({"organization_id": org.organization_id}), 201


@api_bp.route("/users", methods=["POST"])
def create_user():
    """Register a new user and assign role.

    WHY: required for role-based access testing.
    WHAT: closes #user-management
    HOW: Extend with email verification. Roll back by dropping table.
    """
    data = request.get_json() or {}
    user = models.User(
        user_id=str(uuid.uuid4()),
        organization_id=data.get("organization_id"),
        email=data.get("email"),
        password_hash=generate_password_hash(data.get("password", "")),
        role=data.get("role"),
        first_name=data.get("first_name"),
    )
    session: Session = SessionLocal()
    session.add(user)
    session.commit()
    return jsonify({"user_id": user.user_id}), 201


@api_bp.route("/login", methods=["POST"])
def login():
    """Return auth token if credentials are valid."""
    data = request.get_json() or {}
    token = auth.login(data.get("email"), data.get("password"))
    if not token:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"token": token})


@api_bp.route("/inventory", methods=["GET"])
@auth.token_required()
def list_inventory():
    """List inventory records for the user's organization."""
    session: Session = SessionLocal()
    records = session.query(models.Inventory).filter_by(
        organization_id=request.user.organization_id
    ).all()
    out = [
        {
            "inventory_record_id": r.inventory_record_id,
            "product_id": r.product_id,
            "batch_id": r.batch_id,
            "quantity": r.quantity,
        }
        for r in records
    ]
    session.close()
    return jsonify(out)
