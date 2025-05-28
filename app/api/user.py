from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app import database as db
import sqlalchemy

router = APIRouter(prefix="/user", tags=["user"])

# Pydantic schema
class UserCreate(BaseModel):
    name: str

# Create user
@router.post("/create")
def create_user(user: UserCreate):
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("INSERT INTO \"user\" (name) VALUES (:name) RETURNING id"),
            {"name": user.name}
        )
        user_id = result.scalar_one()
    return {"success": True, "id": user_id}

# Delete user by ID
@router.delete("/{user_id}")
def delete_user(user_id: int):
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("DELETE FROM \"user\" WHERE id = :id"),
            {"id": user_id}
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": f"User {user_id} deleted."}
