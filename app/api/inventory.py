from fastapi import APIRouter
from app import database as db
import sqlalchemy

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/")
def get_inventory():
    with db.engine.begin() as conn:
        result = conn.execute(sqlalchemy.text("SELECT sku, amount FROM inventory")).fetchall()

    items = [{"sku": row.sku, "quantity": row.amount} for row in result]
    return {"items": items}
