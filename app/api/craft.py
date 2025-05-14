from fastapi import APIRouter, Query
from app import database as db
import sqlalchemy
from pydantic import BaseModel

router = APIRouter(prefix="/craft", tags=["craft"])

class CraftRequest(BaseModel):
    item_name: str
    quantity: int

ITEM_NAME_TO_SKU = {
    "iron_pickaxe": "IRON_PICKAXE"
}

@router.post("/")
def craft_item(req: CraftRequest):
    with db.engine.begin() as conn:
        # get sku
        item_result = conn.execute(
            sqlalchemy.text("SELECT sku FROM item WHERE LOWER(name) = LOWER(:name)"),
            {"name": req.item_name}
        ).first()

        if not item_result:
            return {"success": False, "error": "Item does not exist"}

        craft_sku = item_result.sku

        # get recipe
        recipe = conn.execute(
            sqlalchemy.text("SELECT id, output_qty FROM recipe WHERE craftable_item = :sku"),
            {"sku": craft_sku}
        ).first()

        if not recipe:
            return {"success": False, "error": "Item is not craftable"}

        recipe_id = recipe.id
        output_qty = recipe.output_qty

        # get ingredient
        ingredients = conn.execute(
            sqlalchemy.text("SELECT item_sku, quantity FROM recipe_ingredients WHERE recipe_id = :recipe_id"),
            {"recipe_id": recipe_id}
        ).fetchall()

        #  check if ingredient in inv
        for ing in ingredients:
            total_needed = ing.quantity * req.quantity
            inv = conn.execute(
                sqlalchemy.text("SELECT amount FROM inventory WHERE sku = :sku"),
                {"sku": ing.item_sku}
            ).first()

            if not inv or inv.amount < total_needed:
                return {
                    "success": False,
                    "error": f"Not enough {ing.item_sku}. Required: {total_needed}, Found: {inv.amount if inv else 0}"
                }

        # minus the ingredients
        for ing in ingredients:
            total_needed = ing.quantity * req.quantity
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount - :qty WHERE sku = :sku"),
                {"qty": total_needed, "sku": ing.item_sku}
            )

        # add item in inv
        total_crafted = output_qty * req.quantity
        existing = conn.execute(
            sqlalchemy.text("SELECT amount FROM inventory WHERE sku = :sku"),
            {"sku": craft_sku}
        ).first()

        if existing:
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount + :qty WHERE sku = :sku"),
                {"qty": total_crafted, "sku": craft_sku}
            )
        else:
            name_result = conn.execute(
                sqlalchemy.text("SELECT name FROM item WHERE sku = :sku"),
                {"sku": craft_sku}
            ).first()
            conn.execute(
                sqlalchemy.text("INSERT INTO inventory (sku, item_name, amount) VALUES (:sku, :name, :qty)"),
                {"sku": craft_sku, "name": name_result.name, "qty": total_crafted}
            )

    return {"success": True, "crafted_quantity": total_crafted}

class RecipeRequest(BaseModel):
    item_name: str 

@router.get("/recipe")
def get_crafting_recipe(item_name: str = Query(..., alias="item_name")):
    item_name = item_name.strip()

    with db.engine.begin() as conn:
        # get da SKU from item name
        sku_result = conn.execute(
            sqlalchemy.text("SELECT sku FROM item WHERE LOWER(name) = LOWER(:item_name)"),
            {"item_name": item_name}
        ).fetchone()

        if not sku_result:
            return {"error": "Item not found"}, 404

        item_sku = sku_result[0]

        # get recipe id for that item
        recipe_result = conn.execute(
            sqlalchemy.text("SELECT id FROM recipe WHERE craftable_item = :sku"),
            {"sku": item_sku}
        ).fetchone()

        if not recipe_result:
            return {"error": "Recipe not found"}, 404

        recipe_id = recipe_result[0]

        # get ingredients for that recipe
        ingredients = conn.execute(
            sqlalchemy.text("""
                SELECT item_sku, quantity
                FROM recipe_ingredients
                WHERE recipe_id = :recipe_id
            """),
            {"recipe_id": recipe_id}
        ).fetchall()

        return {
            "item_name": item_name,
            "ingredients": [
                {"sku": row.item_sku, "quantity": str(row.quantity)}
                for row in ingredients
            ]
        }