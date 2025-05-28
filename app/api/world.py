from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app import database as db
import sqlalchemy
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/world", tags=["world"])

# Utility to get user_id from username
def get_user_id(conn, username: str) -> int:
    user = conn.execute(
        sqlalchemy.text("SELECT id FROM user WHERE name = :username"),
        {"username": username}
    ).first()
    if not user:
        raise ValueError(f"User '{username}' not found.")
    return user.id

# Drop item to the floor
class DropRequest(BaseModel):
    username: str
    sku: str
    quantity: int

@router.post("/drop")
def drop_item(req: DropRequest):
    with db.engine.begin() as conn:
        # Clean up expired floor items
        conn.execute(sqlalchemy.text("DELETE FROM floor WHERE dropped_at < NOW() - INTERVAL '5 minutes'"))

        try:
            user_id = get_user_id(conn, req.username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        inventory = conn.execute(
            sqlalchemy.text("SELECT amount FROM inventory WHERE user_id = :uid AND sku = :sku"),
            {"uid": user_id, "sku": req.sku}
        ).first()

        if not inventory or inventory.amount < req.quantity:
            raise HTTPException(status_code=400, detail="Not enough items to drop")

        conn.execute(
            sqlalchemy.text("UPDATE inventory SET amount = amount - :qty WHERE user_id = :uid AND sku = :sku"),
            {"qty": req.quantity, "uid": user_id, "sku": req.sku}
        )

        conn.execute(
            sqlalchemy.text("""
                INSERT INTO floor (item_sku, quantity, dropped_at)
                VALUES (:sku, :qty, NOW())
            """),
            {"sku": req.sku, "qty": req.quantity}
        )

    return {"success": True, "dropped": req.quantity, "sku": req.sku}

# View all floor items
@router.get("/view")
def view_floor():
    with db.engine.begin() as conn:
        # Clean up expired floor items
        conn.execute(sqlalchemy.text("DELETE FROM floor WHERE dropped_at < NOW() - INTERVAL '5 minutes'"))

        result = conn.execute(
            sqlalchemy.text("""
                SELECT id, item_sku, quantity, dropped_at
                FROM floor
                ORDER BY dropped_at DESC
            """)
        ).fetchall()

    return [
        {
            "id": row.id,
            "sku": row.item_sku,
            "quantity": row.quantity,
            "dropped_at": row.dropped_at.isoformat()
        }
        for row in result
    ]

# Pick up a dropped item
class PickupRequest(BaseModel):
    username: str
    floor_id: int

@router.post("/pickup")
def pickup_item(req: PickupRequest):
    with db.engine.begin() as conn:
        # Clean up expired floor items
        conn.execute(sqlalchemy.text("DELETE FROM floor WHERE dropped_at < NOW() - INTERVAL '5 minutes'"))

        try:
            user_id = get_user_id(conn, req.username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        floor_item = conn.execute(
            sqlalchemy.text("SELECT item_sku, quantity FROM floor WHERE id = :fid"),
            {"fid": req.floor_id}
        ).first()

        if not floor_item:
            raise HTTPException(status_code=404, detail="Item not found on floor")

        existing = conn.execute(
            sqlalchemy.text("SELECT amount FROM inventory WHERE user_id = :uid AND sku = :sku"),
            {"uid": user_id, "sku": floor_item.item_sku}
        ).first()

        if existing:
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount + :qty WHERE user_id = :uid AND sku = :sku"),
                {"qty": floor_item.quantity, "uid": user_id, "sku": floor_item.item_sku}
            )
        else:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO inventory (user_id, sku, amount, favorite)
                    VALUES (:uid, :sku, :qty, FALSE)
                """),
                {"uid": user_id, "sku": floor_item.item_sku, "qty": floor_item.quantity}
            )

        conn.execute(
            sqlalchemy.text("DELETE FROM floor WHERE id = :fid"),
            {"fid": req.floor_id}
        )

    return {"success": True, "picked_up": floor_item.quantity, "sku": floor_item.item_sku}
