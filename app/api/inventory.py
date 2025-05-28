from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from app import database as db
import sqlalchemy

router = APIRouter(prefix="/inventory", tags=["inventory"])

# get user_id from username
def get_user_id(conn, username: str) -> int:
    user = conn.execute(
        sqlalchemy.text('SELECT id FROM "user" WHERE name = :username'),
        {"username": username}
    ).first()

    if not user:
        raise ValueError(f"User '{username}' not found.")
    return user.id

@router.get("/")
def get_inventory(username: str = Query(...)):
    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        result = conn.execute(
            sqlalchemy.text("""
                SELECT sku, item_name, amount, favorite
                FROM inventory
                WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchall()

    return {
        "items": [
            {
                "sku": row.sku,
                "item_name": row.item_name,
                "quantity": row.amount,
                "favorite": row.favorite,
            }
            for row in result
        ]
    }

class FavoriteRequest(BaseModel):
    username: str
    sku: str
    favorite: bool = True

@router.post("/favorite")
def set_favorite(req: FavoriteRequest):
    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, req.username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        result = conn.execute(
            sqlalchemy.text("""
                SELECT 1 FROM inventory WHERE sku = :sku AND user_id = :user_id
            """),
            {"sku": req.sku, "user_id": user_id}
        ).first()

        if not result:
            return {"success": False, "error": "Item not found"}

        conn.execute(
            sqlalchemy.text("""
                UPDATE inventory SET favorite = :fav
                WHERE sku = :sku AND user_id = :user_id
            """),
            {"fav": req.favorite, "sku": req.sku, "user_id": user_id}
        )

    return {"success": True, "sku": req.sku, "favorite": req.favorite}

@router.get("/favorite")
def get_favorites(username: str = Query(...)):
    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        result = conn.execute(
            sqlalchemy.text("""
                SELECT sku, item_name, amount
                FROM inventory
                WHERE favorite = TRUE AND user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchall()

    return {
        "favorites": [
            {"sku": row.sku, "item_name": row.item_name, "quantity": row.amount}
            for row in result
        ]
    }

@router.get("/item", summary="Get all item names")
def get_all_item_names():
    with db.engine.begin() as conn:
        result = conn.execute(sqlalchemy.text("SELECT name FROM item")).fetchall()
    return [row.name for row in result]

@router.get("/tools", summary="Get all tools in inventory")
def get_tools_in_inventory(username: str = Query(...)):
    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        result = conn.execute(
            sqlalchemy.text("""
                SELECT inventory.sku, inventory.item_name, inventory.amount, inventory.favorite
                FROM inventory
                JOIN item ON inventory.sku = item.sku
                WHERE item.type = 'Tool' AND inventory.user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchall()

    return {
        "tools": [
            {
                "sku": row.sku,
                "item_name": row.item_name,
                "quantity": row.amount,
                "favorite": row.favorite,
            }
            for row in result
        ]
    }

@router.get("/ores", summary="Get all ores in inventory")
def get_ores_in_inventory(username: str = Query(...)):
    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        result = conn.execute(
            sqlalchemy.text("""
                SELECT inventory.sku, inventory.item_name, inventory.amount, inventory.favorite
                FROM inventory
                JOIN item ON inventory.sku = item.sku
                WHERE item.type = 'ore' AND inventory.user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchall()

    return {
        "ores": [
            {
                "sku": row.sku,
                "item_name": row.item_name,
                "quantity": row.amount,
                "favorite": row.favorite,
            }
            for row in result
        ]
    }

@router.get("/blocks", summary="Get all blocks in inventory")
def get_blocks_in_inventory(username: str = Query(...)):
    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        result = conn.execute(
            sqlalchemy.text("""
                SELECT inventory.sku, inventory.item_name, inventory.amount, inventory.favorite
                FROM inventory
                JOIN item ON inventory.sku = item.sku
                WHERE item.type = 'block' AND inventory.user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchall()

    return {
        "blocks": [
            {
                "sku": row.sku,
                "item_name": row.item_name,
                "quantity": row.amount,
                "favorite": row.favorite,
            }
            for row in result
        ]
    }
