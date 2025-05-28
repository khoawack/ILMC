from fastapi import APIRouter
from app import database as db
import sqlalchemy

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/reset")
def reset_users_and_inventory():
    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text("DELETE FROM inventory"))
        conn.execute(sqlalchemy.text('DELETE FROM "user"'))
    return {"success": True, "message": "All users and inventory have been reset."}
