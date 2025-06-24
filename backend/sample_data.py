"""Seed data for development/testing."""

import uuid
from werkzeug.security import generate_password_hash
from .database import SessionLocal
from . import models


def seed():
    """Insert sample organizations, users, and products if not already present."""
    session = SessionLocal()
    if session.query(models.Organization).first():
        session.close()
        return

    manuf = models.Organization(
        organization_id="MANUF001",
        name="Sample Manufacturer",
        type="Manufacturer",
    )
    cfa = models.Organization(
        organization_id="CFA001",
        name="Sample CFA",
        type="CFA",
        parent_organization_id=manuf.organization_id,
    )
    stock = models.Organization(
        organization_id="STOCK001",
        name="Sample Stockist",
        type="Stockist",
        parent_organization_id=cfa.organization_id,
    )
    session.add_all([manuf, cfa, stock])

    users = [
        models.User(
            user_id=str(uuid.uuid4()),
            organization_id=manuf.organization_id,
            email="manuf@example.com",
            password_hash=generate_password_hash("password"),
            role="manufacturer",
            first_name="Manu",
        ),
        models.User(
            user_id=str(uuid.uuid4()),
            organization_id=cfa.organization_id,
            email="cfa@example.com",
            password_hash=generate_password_hash("password"),
            role="cfa",
            first_name="Cfa",
        ),
        models.User(
            user_id=str(uuid.uuid4()),
            organization_id=stock.organization_id,
            email="stock@example.com",
            password_hash=generate_password_hash("password"),
            role="stockist",
            first_name="Stock",
        ),
    ]
    session.add_all(users)

    product = models.Product(
        product_id="PROD001",
        name="PainRelief",
        sku="PR-100",
        description="Sample product",
        unit_of_measure="box",
        manufacturer_org_id=manuf.organization_id,
    )
    session.add(product)

    batch = models.Batch(
        batch_id="BATCH001",
        product_id=product.product_id,
        batch_number="B-001",
        manufacturing_site_name="Site A",
    )
    session.add(batch)

    inventory = models.Inventory(
        inventory_record_id=str(uuid.uuid4()),
        organization_id=manuf.organization_id,
        product_id=product.product_id,
        batch_id=batch.batch_id,
        quantity=100,
    )
    session.add(inventory)

    session.commit()
    session.close()
