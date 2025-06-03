from fastapi import APIRouter
from app import database as db
import sqlalchemy

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/reset")
def reset_users_and_inventory():
    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
        TRUNCATE TABLE
            collection_log,
            inventory,
            floor,
            "user"
        RESTART IDENTITY CASCADE;
    """))
    return {"success": True, "message": "All users and inventory have been reset."}
