from fastapi import APIRouter
from app import database as db
import sqlalchemy
import random
from fastapi import Request
from pydantic import BaseModel

router = APIRouter(prefix="/action", tags=["action"])

BASIC_ITEMS = [
    {"sku": "WOOD_PLANK", "name": "Wooden Plank"},
    {"sku": "DIRT", "name": "Dirt"},
    {"sku": "SEED", "name": "Seed"},
]

@router.post("/collect")
def collect_item():
    item = random.choice(BASIC_ITEMS)
    quantity = random.randint(1, 3)

    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT amount FROM inventory WHERE sku = :sku"),
            {"sku": item["sku"]}
        ).first()

        if result:
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount + :qty WHERE sku = :sku"),
                {"qty": quantity, "sku": item["sku"]}
            )
        else:
            conn.execute(
                sqlalchemy.text(
                    "INSERT INTO inventory (sku, item_name, amount) VALUES (:sku, :name, :qty)"
                ),
                {"sku": item["sku"], "name": item["name"], "qty": quantity}
            )

    return {
        "item_name": item["name"],
        "sku": item["sku"],
        "quantity": quantity
    }

class MineRequest(BaseModel):
    pickaxe_name: str

# ores drop odds tables
DROP_TABLES = {
    "Wooden Pickaxe": [("COBBLESTONE", 1.0)],
    "Stone Pickaxe": [("COBBLESTONE", 0.75), ("IRON", 0.25)],
    "Iron Pickaxe": [("COBBLESTONE", 0.5), ("IRON", 0.3), ("GOLD", 0.15), ("DIAMOND", 0.05)],
    "Gold Pickaxe": [("COBBLESTONE", 0.2), ("IRON", 0.6), ("GOLD", 0.12), ("DIAMOND", 0.08)],
    "Diamond Pickaxe": [("COBBLESTONE", 0.1), ("IRON", 0.5), ("GOLD", 0.25), ("DIAMOND", 0.15)],
}

def random_ore(pickaxe_name: str) -> str:
    drops = DROP_TABLES.get(pickaxe_name)
    if not drops:
        return None
    roll = random.random()
    cumulative = 0
    for sku, prob in drops:
        cumulative += prob
        if roll <= cumulative:
            return sku
    return drops[-1][0]

@router.post("/mine")
def mine_ores(body: MineRequest):
    pickaxe_name = body.pickaxe_name.strip()

    mined_sku = random_ore(pickaxe_name)
    if not mined_sku:
        return {"error": "Invalid pickaxe name"}, 400

    quantity = random.randint(1, 3)

    with db.engine.begin() as conn:
        # check if item already exists in inventory
        existing = conn.execute(
            sqlalchemy.text("SELECT amount FROM inventory WHERE sku = :sku"),
            {"sku": mined_sku}
        ).fetchone()

        if existing:
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount + :qty WHERE sku = :sku"),
                {"qty": quantity, "sku": mined_sku}
            )
        else:
            # get name from item table
            mined_name = conn.execute(
                sqlalchemy.text("SELECT name FROM item WHERE sku = :sku"),
                {"sku": mined_sku}
            ).scalar() or mined_sku

            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO inventory (sku, item_name, amount, favorite)
                    VALUES (:sku, :name, :qty, FALSE)
                """),
                {"sku": mined_sku, "name": mined_name, "qty": quantity}
            )

    return {"sku": mined_sku, "quantity": quantity}