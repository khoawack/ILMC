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
