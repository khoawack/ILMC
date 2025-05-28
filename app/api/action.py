from fastapi import APIRouter, Query, HTTPException
from app import database as db
import sqlalchemy
import random
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/action", tags=["action"])

BASIC_ITEMS = [
    {"sku": "WOOD_PLANK", "name": "Wooden Plank"},
    {"sku": "DIRT", "name": "Dirt"},
    {"sku": "SEED", "name": "Seed"},
]

# Get user_id from username
def get_user_id(conn, username: str) -> int:
    user = conn.execute(
        sqlalchemy.text('SELECT id FROM "user" WHERE name = :username'),
        {"username": username}
    ).first()

    if not user:
        raise ValueError(f"User '{username}' not found.")
    return user.id

@router.post("/collect")
def collect_item(username: str = Query(...)):
    item = random.choice(BASIC_ITEMS)
    quantity = random.randint(1, 3)

    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        # Clean old collection logs
        conn.execute(sqlalchemy.text("DELETE FROM collection_log WHERE collected_at < NOW() - INTERVAL '1 day'"))

        # Cooldown check
        recent = conn.execute(
            sqlalchemy.text("""
                SELECT collected_at FROM collection_log
                WHERE user_id = :user_id
                ORDER BY collected_at DESC
                LIMIT 1
            """),
            {"user_id": user_id}
        ).scalar()

        if recent and (datetime.now(timezone.utc) - recent) < timedelta(seconds=10):
            raise HTTPException(status_code=429, detail="Collect cooldown: wait a few seconds")

        result = conn.execute(
            sqlalchemy.text("""
                SELECT amount FROM inventory
                WHERE sku = :sku AND user_id = :user_id
            """),
            {"sku": item["sku"], "user_id": user_id}
        ).first()

        if result:
            conn.execute(
                sqlalchemy.text("""
                    UPDATE inventory
                    SET amount = amount + :qty
                    WHERE sku = :sku AND user_id = :user_id
                """),
                {"qty": quantity, "sku": item["sku"], "user_id": user_id}
            )
        else:
            item_name = conn.execute(
                sqlalchemy.text("SELECT name FROM item WHERE sku = :sku"),
                {"sku": item["sku"]}
            ).scalar() or item["name"]

            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO inventory (user_id, sku, item_name, amount, favorite)
                    VALUES (:user_id, :sku, :item_name, :qty, FALSE)
                """),
                {"user_id": user_id, "sku": item["sku"], "item_name": item_name, "qty": quantity}
            )

        # Log the collection in collection_log
        conn.execute(
            sqlalchemy.text("""
                INSERT INTO collection_log (user_id, item_sku, quantity_collected, collected_at)
                VALUES (:user_id, :sku, :qty, NOW())
            """),
            {"user_id": user_id, "sku": item["sku"], "qty": quantity}
        )

    return {
        "item_name": item["name"],
        "sku": item["sku"],
        "quantity": quantity
    }

class MineRequest(BaseModel):
    pickaxe_name: str
    username: str

def random_ore(pickaxe_sku: str) -> str | None:
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("""
                SELECT item_sku, drop_chance
                FROM drop_rates
                WHERE pickaxe_sku = :pickaxe
            """),
            {"pickaxe": pickaxe_sku}
        ).fetchall()

    if not result:
        return None

    roll = random.random()
    cumulative = 0
    for row in result:
        cumulative += row.drop_chance
        if roll <= cumulative:
            return row.item_sku

    return result[-1].item_sku

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

@router.post("/mine")
def mine_ores(body: MineRequest):
    pickaxe_name = body.pickaxe_name.strip()
    mined_sku = random_ore(pickaxe_name)

    if not mined_sku:
        raise HTTPException(status_code=400, detail="Invalid pickaxe name")

    quantity = random.randint(1, 3)

    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, body.username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        # Clean old collection logs
        conn.execute(sqlalchemy.text("DELETE FROM collection_log WHERE collected_at < NOW() - INTERVAL '1 day'"))

        # Cooldown check
        recent = conn.execute(
            sqlalchemy.text("""
                SELECT collected_at FROM collection_log
                WHERE user_id = :user_id
                ORDER BY collected_at DESC
                LIMIT 1
            """),
            {"user_id": user_id}
        ).scalar()

        if recent and (datetime.now(timezone.utc) - recent) < timedelta(seconds=10):
            raise HTTPException(status_code=429, detail="Mine cooldown: wait a few seconds")

        existing = conn.execute(
            sqlalchemy.text("""
                SELECT amount FROM inventory
                WHERE sku = :sku AND user_id = :user_id
            """),
            {"sku": mined_sku, "user_id": user_id}
        ).fetchone()

        if existing:
            conn.execute(
                sqlalchemy.text("""
                    UPDATE inventory
                    SET amount = amount + :qty
                    WHERE sku = :sku AND user_id = :user_id
                """),
                {"qty": quantity, "sku": mined_sku, "user_id": user_id}
            )
        else:
            mined_name = conn.execute(
                sqlalchemy.text("SELECT name FROM item WHERE sku = :sku"),
                {"sku": mined_sku}
            ).scalar() or mined_sku

            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO inventory (user_id, sku, item_name, amount, favorite)
                    VALUES (:user_id, :sku, :item_name, :qty, FALSE)
                """),
                {"user_id": user_id, "sku": mined_sku, "item_name": mined_name, "qty": quantity}
            )

        # Log the mining in collection_log
        conn.execute(
            sqlalchemy.text("""
                INSERT INTO collection_log (user_id, item_sku, quantity_collected, collected_at)
                VALUES (:user_id, :sku, :qty, NOW())
            """),
            {"user_id": user_id, "sku": mined_sku, "qty": quantity}
        )

    return {"sku": mined_sku, "quantity": quantity}
