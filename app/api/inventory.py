from fastapi import APIRouter
from pydantic import BaseModel
from app import database as db
import sqlalchemy

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/")
def get_inventory():
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT sku, item_name, amount, favorite FROM inventory")
        ).fetchall()

    items = [
        {
            "sku": row.sku,
            "item_name": row.item_name,
            "quantity": row.amount,
            "favorite": row.favorite,
        }
        for row in result
    ]
    return {"items": items}


class FavoriteRequest(BaseModel):
    sku: str
    favorite: bool = True

@router.post("/favorite")
def set_favorite(req: FavoriteRequest):
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT 1 FROM inventory WHERE sku = :sku"),
            {"sku": req.sku}
        ).first()

        if not result:
            return {"success": False, "error": "Item not found"}

        conn.execute(
            sqlalchemy.text("UPDATE inventory SET favorite = :fav WHERE sku = :sku"),
            {"fav": req.favorite, "sku": req.sku}
        )

    return {"success": True, "sku": req.sku, "favorite": req.favorite}


@router.get("/favorite")
def get_favorites():
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT sku, item_name, amount FROM inventory WHERE favorite = TRUE")
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
        result = conn.execute(
            sqlalchemy.text("SELECT name FROM item")
        ).fetchall()
        return [row.name for row in result]
    

@router.get("/tools", summary="Get all tools in inventory")
def get_tools_in_inventory():
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("""
                SELECT inventory.sku, inventory.item_name, inventory.amount, inventory.favorite
                FROM inventory
                JOIN item ON inventory.sku = item.sku
                WHERE item.type = 'Tool'
            """)
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
def get_ores_in_inventory():
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("""
                SELECT inventory.sku, inventory.item_name, inventory.amount, inventory.favorite
                FROM inventory
                JOIN item ON inventory.sku = item.sku
                WHERE item.type = 'ore'
            """)
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
def get_blocks_in_inventory():
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("""
                SELECT inventory.sku, inventory.item_name, inventory.amount, inventory.favorite
                FROM inventory
                JOIN item ON inventory.sku = item.sku
                WHERE item.type = 'block'
            """)
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

