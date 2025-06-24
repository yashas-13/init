"""Flask routes exposing basic CRUD operations and authentication."""

from flask import Blueprint, request, jsonify, g
from .version import VERSION
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models
import uuid
import hashlib

# In-memory token store for demo purposes
tokens = {}


def hash_password(password: str) -> str:
    """Return SHA256 hash of password."""
    return hashlib.sha256(password.encode()).hexdigest()


def require_auth(role: str | None = None):
    """Decorator to require valid token and optional role."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            token = auth.replace("Bearer ", "")
            user_id = tokens.get(token)
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            session = SessionLocal()
            user = session.get(models.User, user_id)
            if not user:
                return jsonify({"error": "Unauthorized"}), 401
            if role and user.role != role:
                return jsonify({"error": "Forbidden"}), 403
            g.current_user = user
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator

api_bp = Blueprint("api", __name__)


@api_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a token."""
    data = request.get_json() or {}
    session = SessionLocal()
    user = session.query(models.User).filter_by(email=data.get("email")).first()
    if not user or user.password_hash != hash_password(data.get("password", "")):
        return jsonify({"error": "Invalid credentials"}), 401
    token = str(uuid.uuid4())
    tokens[token] = user.user_id
    return jsonify({"token": token})


@api_bp.route("/version", methods=["GET"])
def get_version():
    """Return backend version.

    WHY: allow clients to verify API compatibility.
    WHAT: closes #improve-readme
    HOW: update VERSION constant or remove route to roll back.
    """
    return jsonify({"version": VERSION})


@api_bp.route("/organizations", methods=["POST"])
@require_auth(role="Manufacturer")
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
@require_auth(role="Manufacturer")
def create_user():
    """Add a new user linked to an organization."""
    data = request.get_json() or {}
    session = SessionLocal()
    user = models.User(
        user_id=data.get("user_id") or str(uuid.uuid4()),
        organization_id=data.get("organization_id"),
        email=data.get("email"),
        password_hash=hash_password(data.get("password", "")),
        role=data.get("role"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
    )
    session.add(user)
    session.commit()
    return jsonify({"user_id": user.user_id}), 201


@api_bp.route("/products", methods=["POST"])
@require_auth(role="Manufacturer")
def create_product():
    """Create a product entry."""
    data = request.get_json() or {}
    session = SessionLocal()
    prod = models.Product(
        product_id=data.get("product_id") or str(uuid.uuid4()),
        name=data.get("name"),
        sku=data.get("sku"),
        manufacturer_org_id=data.get("manufacturer_org_id"),
    )
    session.add(prod)
    session.commit()
    return jsonify({"product_id": prod.product_id}), 201


@api_bp.route("/inventory", methods=["POST"])
@require_auth()
def add_inventory():
    """Record inventory quantities by batch."""
    data = request.get_json() or {}
    session = SessionLocal()
    inv = models.Inventory(
        inventory_record_id=str(uuid.uuid4()),
        organization_id=data.get("organization_id"),
        product_id=data.get("product_id"),
        batch_id=data.get("batch_id"),
        quantity=data.get("quantity"),
    )
    session.add(inv)
    session.commit()
    return jsonify({"inventory_record_id": inv.inventory_record_id}), 201


@api_bp.route("/requests", methods=["POST"])
@require_auth()
def create_request():
    """Submit a dispatch or return request."""
    data = request.get_json() or {}
    session = SessionLocal()
    req = models.Request(
        request_id=str(uuid.uuid4()),
        request_type=data.get("request_type"),
        initiator_user_id=g.current_user.user_id,
        initiator_org_id=g.current_user.organization_id,
        target_org_id=data.get("target_org_id"),
        notes=data.get("notes"),
    )
    session.add(req)
    session.commit()
    return jsonify({"request_id": req.request_id}), 201


@api_bp.route("/approvals", methods=["POST"])
@require_auth()
def approve_request():
    """Record an approval step for a request."""
    data = request.get_json() or {}
    session = SessionLocal()
    appr = models.Approval(
        approval_record_id=str(uuid.uuid4()),
        request_id=data.get("request_id"),
        approver_user_id=g.current_user.user_id,
        approval_step=data.get("approval_step", 1),
        status=data.get("status"),
    )
    session.add(appr)
    session.commit()
    return jsonify({"approval_record_id": appr.approval_record_id}), 201


@api_bp.route("/audit-logs", methods=["GET"])
@require_auth()
def list_audit_logs():
    """Return all audit logs."""
    session = SessionLocal()
    logs = session.query(models.AuditLog).all()
    return jsonify([
        {
            "log_id": l.log_id,
            "action_type": l.action_type,
            "table_name": l.table_name,
            "record_id": l.record_id,
            "timestamp": l.timestamp.isoformat(),
        }
        for l in logs
    ])