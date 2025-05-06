from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# ---------------------
# Item
# ---------------------
class Item(Base):
    __tablename__ = "items"

    sku = Column(Text, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    type = Column(Text)

    inventory_items = relationship("Inventory", back_populates="item")
    collection_logs = relationship("CollectionLog", back_populates="item")
    recipes = relationship("Recipe", back_populates="output_item")
    ingredient_in = relationship("RecipeIngredient", back_populates="item")


# ---------------------
# Inventory
# ---------------------
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(Text, ForeignKey("items.sku"), nullable=False)
    item_name = Column(Text)
    favorite = Column(Boolean, default=False)
    amount = Column(Integer, default=0)

    item = relationship("Item", back_populates="inventory_items")


# ---------------------
# Collection Log
# ---------------------
class CollectionLog(Base):
    __tablename__ = "collection_log"

    id = Column(Integer, primary_key=True, index=True)
    item_sku = Column(Text, ForeignKey("items.sku"), nullable=False)
    quantity_collected = Column(Integer)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())

    item = relationship("Item", back_populates="collection_logs")


# ---------------------
# Recipe
# ---------------------
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    craftable_item = Column(Text, ForeignKey("items.sku"), nullable=False)
    output_qty = Column(Integer, default=1)

    output_item = relationship("Item", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")


# ---------------------
# RecipeIngredient
# ---------------------
class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    item_sku = Column(Text, ForeignKey("items.sku"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")
    item = relationship("Item", back_populates="ingredient_in")
