from sqlalchemy import Column, Text, Integer, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(Text, nullable=False)
    item_name = Column(Text, nullable=False)
    favorite = Column(Boolean, default=False)
    amount = Column(Integer, default=0)


class Item(Base):
    __tablename__ = "item"

    sku = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    type = Column(Text)

    recipes = relationship("Recipe", back_populates="crafted_item_rel")
    ingredients_in = relationship("RecipeIngredient", back_populates="item_rel")


class CollectionLog(Base):
    __tablename__ = "collection_log"

    id = Column(Integer, primary_key=True, index=True)
    item_sku = Column(Text, ForeignKey("item.sku"))
    quantity_collected = Column(Text)
    collected_at = Column(TIMESTAMP(timezone=True))

    item_rel = relationship("Item")


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    craftable_item = Column(Text, ForeignKey("item.sku"))
    output_qty = Column(Integer)

    crafted_item_rel = relationship("Item", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe_rel")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
    item_sku = Column(Text, ForeignKey("item.sku"), primary_key=True)
    quantity = Column(Integer)

    recipe_rel = relationship("Recipe", back_populates="ingredients")
    item_rel = relationship("Item", back_populates="ingredients_in")
