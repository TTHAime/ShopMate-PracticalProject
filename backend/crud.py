from __future__ import annotations

import secrets
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Tenant


def create_tenant(db: Session, name: str) -> tuple[str, str]:
    """
    Create tenant and return (tenant_id, public_token)
    """
    token = secrets.token_urlsafe(24)
    t = Tenant(name=name.strip(), public_token=token)
    db.add(t)
    db.commit()
    db.refresh(t)
    return str(t.id), t.public_token


def get_tenant_by_token(db: Session, token: str) -> Tenant | None:
    return db.scalar(select(Tenant).where(Tenant.public_token == token))


def get_tenant_by_id(db: Session, tenant_id: str) -> Tenant | None:
    return db.get(Tenant, tenant_id)
