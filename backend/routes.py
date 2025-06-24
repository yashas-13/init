"""Flask routes exposing basic CRUD operations."""

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models
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
