from fastapi import APIRouter, Query, HTTPException
from app import database as db
import sqlalchemy
from pydantic import BaseModel, Field
from app.api.action import get_user_id

router = APIRouter(prefix="/craft", tags=["craft"])

class CraftRequest(BaseModel):
    sku: str  # changed from item_name to sku
    quantity: int = Field(gt=0, description="Must be at least 1")
    username: str


@router.post("/")
def craft_item(req: CraftRequest):
    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, req.username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        craft_sku = req.sku.strip().upper()

        # get recipe
        recipe = conn.execute(
            sqlalchemy.text("SELECT id, output_qty FROM recipe WHERE craftable_item = :sku"),
            {"sku": craft_sku}
        ).first()

        if not recipe:
            return {"success": False, "error": "Item is not craftable"}

        recipe_id = recipe.id
        output_qty = recipe.output_qty

        # get ingredients
        ingredients = conn.execute(
            sqlalchemy.text("SELECT item_sku, quantity FROM recipe_ingredients WHERE recipe_id = :recipe_id"),
            {"recipe_id": recipe_id}
        ).fetchall()

        # check if ingredients are in inventory
        for ing in ingredients:
            total_needed = ing.quantity * req.quantity
            inv = conn.execute(
                sqlalchemy.text("SELECT amount FROM inventory WHERE sku = :sku AND user_id = :user_id"),
                {"sku": ing.item_sku, "user_id": user_id}
            ).first()

            if not inv or inv.amount < total_needed:
                return {
                    "success": False,
                    "error": f"Not enough {ing.item_sku}. Required: {total_needed}, Found: {inv.amount if inv else 0}"
                }
        #subtract ingredients
        for ing in ingredients:
            total_needed = ing.quantity * req.quantity
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount - :qty WHERE sku = :sku AND user_id = :user_id"),
                {"qty": total_needed, "sku": ing.item_sku, "user_id": user_id}
            )
            conn.execute(
                sqlalchemy.text("DELETE FROM inventory WHERE user_id = :user_id AND sku = :sku AND amount <= 0"),
                {"user_id": user_id, "sku": ing.item_sku}
            )

        # add crafted item to inventory
        total_crafted = output_qty * req.quantity
        existing = conn.execute(
            sqlalchemy.text("SELECT amount FROM inventory WHERE sku = :sku AND user_id = :user_id"),
            {"sku": craft_sku, "user_id": user_id}
        ).first()

        if existing:
            conn.execute(
                sqlalchemy.text("UPDATE inventory SET amount = amount + :qty WHERE sku = :sku AND user_id = :user_id"),
                {"qty": total_crafted, "sku": craft_sku, "user_id": user_id}
            )
        else:
            item_name = conn.execute(
                sqlalchemy.text("SELECT name FROM item WHERE sku = :sku"),
                {"sku": craft_sku}
            ).scalar() or craft_sku

            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO inventory (user_id, sku, item_name, amount, favorite)
                    VALUES (:user_id, :sku, :item_name, :qty, FALSE)
                """),
                {"user_id": user_id, "sku": craft_sku, "item_name": item_name, "qty": total_crafted}
            )

    return {"success": True, "crafted_quantity": total_crafted}


class RecipeRequest(BaseModel):
    sku: str  # changed from item_name to sku

@router.get("/recipe")
def get_crafting_recipe(sku: str = Query(..., alias="sku")):
    sku = sku.strip().upper()

    with db.engine.begin() as conn:
        recipe_result = conn.execute(
            sqlalchemy.text("SELECT id FROM recipe WHERE craftable_item = :sku"),
            {"sku": sku}
        ).fetchone()

        if not recipe_result:
            return {"error": "Recipe not found"}, 404

        recipe_id = recipe_result[0]

        ingredients = conn.execute(
            sqlalchemy.text("""
                SELECT item_sku, quantity
                FROM recipe_ingredients
                WHERE recipe_id = :recipe_id
            """),
            {"recipe_id": recipe_id}
        ).fetchall()

        return {
            "craftable_item": sku,
            "ingredients": [
                {"sku": row.item_sku, "quantity": str(row.quantity)}
                for row in ingredients
            ]
        }

@router.get("/item", summary="Get all craftable item SKUs")
def get_all_craftable_skus():
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT craftable_item FROM recipe")
        ).fetchall()
        return [row.craftable_item for row in result]

@router.get("/available")
def get_craftable_items(username: str = Query(...)):
    craftable = []

    with db.engine.begin() as conn:
        try:
            user_id = get_user_id(conn, username)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

        inventory_rows = conn.execute(
            sqlalchemy.text("SELECT sku, amount FROM inventory WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchall()
        inventory = {row.sku: row.amount for row in inventory_rows}

        recipes = conn.execute(
            sqlalchemy.text("SELECT id, craftable_item, output_qty FROM recipe")
        ).fetchall()

        for recipe in recipes:
            recipe_id = recipe.id
            craftable_sku = recipe.craftable_item
            output_qty = recipe.output_qty

            ingredients = conn.execute(
                sqlalchemy.text("SELECT item_sku, quantity FROM recipe_ingredients WHERE recipe_id = :recipe_id"),
                {"recipe_id": recipe_id}
            ).fetchall()

            can_craft = True
            for ing in ingredients:
                if ing.item_sku not in inventory or inventory[ing.item_sku] < ing.quantity:
                    can_craft = False
                    break

            if can_craft:
                craftable.append({
                    "sku": craftable_sku,
                    "output_quantity": output_qty
                })

    return {"craftable": craftable}
