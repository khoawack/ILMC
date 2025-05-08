from fastapi import APIRouter
from app import database as db
import sqlalchemy

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/reset")
def reset_inventory():
    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text("DELETE FROM inventory"))
    return {"success": True, "message": "Inventory has been reset."}
