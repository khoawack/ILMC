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

    
    