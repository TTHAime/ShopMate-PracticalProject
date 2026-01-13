from __future__ import annotations

from fastapi import Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Tenant


def get_tenant_id(
    db: Session,
    x_shop_token: str | None = Header(default=None),
) -> str:
    """
    Resolve tenant_id from X-Shop-Token.
    Return tenant UUID as string.
    """
    if not x_shop_token:
        raise HTTPException(status_code=401, detail="Missing X-Shop-Token")

    tenant = db.scalar(select(Tenant).where(Tenant.public_token == x_shop_token))
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid shop token")

    return str(tenant.id)
