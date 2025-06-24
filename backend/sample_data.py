"""Seed sample data for testing authentication and feature operations.

WHY: Provide initial orgs, users, and products so devs can immediately test
login and CRUD endpoints.
WHAT: closes #seed-data
HOW: Extend with more sample batches. Roll back by removing this file.
"""

import uuid
from .database import SessionLocal
from . import models
from .routes import hash_password


def seed_data():
    """Insert example organizations, users, and a product if DB is empty."""
    session = SessionLocal()
    if session.query(models.Organization).first():
        session.close()
        return

    manuf = models.Organization(
        organization_id="MANUF1",
        name="Acme Pharma",
        type="Manufacturer",
    )
    cfa = models.Organization(
        organization_id="CFA1",
        name="Central CFA",
        type="CFA",
        parent_organization_id="MANUF1",
    )
    stock = models.Organization(
        organization_id="STOCK1",
        name="City Stockist",
        type="Stockist",
        parent_organization_id="CFA1",
    )
    session.add_all([manuf, cfa, stock])

    admin = models.User(
        user_id="USR1",
        organization_id="MANUF1",
        email="admin@pharma.com",
        password_hash=hash_password("adminpass"),
        role="Manufacturer",
        first_name="Admin",
        last_name="User",
    )
    cfa_user = models.User(
        user_id="USR2",
        organization_id="CFA1",
        email="cfa@pharma.com",
        password_hash=hash_password("cfapass"),
        role="CFA",
    )
    stock_user = models.User(
        user_id="USR3",
        organization_id="STOCK1",
        email="stock@pharma.com",
        password_hash=hash_password("stockpass"),
        role="Stockist",
    )
    session.add_all([admin, cfa_user, stock_user])

    prod = models.Product(
        product_id="PROD1",
        name="Pain Reliever",
        sku="PR001",
        manufacturer_org_id="MANUF1",
    )
    session.add(prod)

    session.commit()
    session.close()
