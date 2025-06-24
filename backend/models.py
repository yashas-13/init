"""SQLAlchemy models for pharmaceutical SCM app.

Derived from dbsetup.md schema. Each table includes timestamps for auditing.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    address = Column(Text)
    city = Column(Text)
    state = Column(Text)
    country = Column(Text)
    postal_code = Column(Text)
    phone = Column(Text)
    fax = Column(Text)
    email = Column(Text)
    parent_organization_id = Column(String, ForeignKey("organizations.organization_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("Organization", remote_side=[organization_id])


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    organization_id = Column(String, ForeignKey("organizations.organization_id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    first_name = Column(Text)
    last_name = Column(Text)
    role = Column(Text, nullable=False)
    status = Column(Text, default="active")
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    description = Column(Text)
    unit_of_measure = Column(Text)
    manufacturer_org_id = Column(String, ForeignKey("organizations.organization_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Batch(Base):
    __tablename__ = "batches"

    batch_id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    batch_number = Column(String, nullable=False)
    manufacturing_date = Column(Date)
    expiry_date = Column(Date)
    manufacturing_site_name = Column(Text)
    quality_control_status = Column(Text, default="Released")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("product_id", "batch_number", name="uix_product_batch"),
    )


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_record_id = Column(String, primary_key=True)
    organization_id = Column(String, ForeignKey("organizations.organization_id"), nullable=False)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    batch_id = Column(String, ForeignKey("batches.batch_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    storage_condition = Column(Text)
    last_updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("organization_id", "batch_id", name="uix_org_batch"),
    )


class Request(Base):
    __tablename__ = "requests"

    request_id = Column(String, primary_key=True)
    request_type = Column(Text, nullable=False)
    initiator_user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    initiator_org_id = Column(String, ForeignKey("organizations.organization_id"), nullable=False)
    target_org_id = Column(String, ForeignKey("organizations.organization_id"))
    status = Column(Text, default="Pending")
    request_date = Column(DateTime, default=datetime.utcnow)
    completion_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class RequestItem(Base):
    __tablename__ = "request_items"

    request_item_id = Column(String, primary_key=True)
    request_id = Column(String, ForeignKey("requests.request_id"), nullable=False)
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    batch_id = Column(String, ForeignKey("batches.batch_id"), nullable=False)
    requested_quantity = Column(Integer, nullable=False)
    approved_quantity = Column(Integer)
    unit_price = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Approval(Base):
    __tablename__ = "approvals"

    approval_record_id = Column(String, primary_key=True)
    request_id = Column(String, ForeignKey("requests.request_id"), nullable=False)
    approver_user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    approval_step = Column(Integer, nullable=False)
    status = Column(Text, nullable=False)
    approval_date = Column(DateTime, default=datetime.utcnow)
    rationale = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("request_id", "approval_step", name="uix_request_step"),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)
    request_id = Column(String, ForeignKey("requests.request_id"))
    product_id = Column(String, ForeignKey("products.product_id"), nullable=False)
    batch_id = Column(String, ForeignKey("batches.batch_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_type = Column(Text, nullable=False)
    source_org_id = Column(String, ForeignKey("organizations.organization_id"))
    destination_org_id = Column(String, ForeignKey("organizations.organization_id"))
    transaction_date = Column(DateTime, default=datetime.utcnow)
    recorded_by_user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    action_type = Column(Text, nullable=False)
    table_name = Column(Text)
    record_id = Column(Text)
    old_value = Column(Text)
    new_value = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

