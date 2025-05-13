from fastapi import APIRouter
from app import database as db
import sqlalchemy
from pydantic import BaseModel

router = APIRouter(prefix="/action", tags=["action"])

class CraftRequest(BaseModel):
    item_name: str
    quantity: int

ITEM_NAME_TO_SKU = {
    "iron_pickaxe": "IRON_PICKAXE"
}

@router.post("/craft")
def craft_item(req: CraftRequest):
    sku = ITEM_NAME_TO_SKU.get(req.item_name.lower())
    if not sku:
        return {"success": False, "error": "Invalid item_name"}

    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT amount FROM inventory WHERE sku = :sku"),
            {"sku": sku}
        ).first()

        if result:
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount + :qty WHERE sku = :sku"),
                {"qty": req.quantity, "sku": sku}
            )
        else:
            conn.execute(
                sqlalchemy.text("INSERT INTO inventory (sku, item_name, amount) VALUES (:sku, :name, :qty)"),
                {"sku": sku, "name": req.item_name, "qty": req.quantity}
            )

    return {"success": True, "crafted_quantity": req.quantity}
