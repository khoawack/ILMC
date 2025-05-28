from sqlalchemy import Column, Text, Integer, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class Item(Base):
    __tablename__ = "item"

    sku = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    type = Column(Text)

    inventory_items = relationship("Inventory", back_populates="item")
    collection_logs = relationship("CollectionLog", back_populates="item")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="item")
    recipe = relationship("Recipe", back_populates="crafted_item", uselist=False)


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  #user id
    sku = Column(Text, ForeignKey("item.sku"), nullable=False)
    item_name = Column(Text, nullable=False)
    favorite = Column(Boolean, default=False)
    amount = Column(Integer, default=0)

    item = relationship("Item", back_populates="inventory_items")
    user = relationship("User")


class CollectionLog(Base):
    __tablename__ = "collection_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  
    item_sku = Column(Text, ForeignKey("item.sku"), nullable=False)
    quantity_collected = Column(Integer)
    collected_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    item = relationship("Item", back_populates="collection_logs")
    user = relationship("User")  


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    craftable_item = Column(Text, ForeignKey("item.sku"), unique=True)
    output_qty = Column(Integer)

    crafted_item = relationship("Item", back_populates="recipe")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
    item_sku = Column(Text, ForeignKey("item.sku"), primary_key=True)
    quantity = Column(Integer)

    recipe = relationship("Recipe", back_populates="ingredients")
    item = relationship("Item", back_populates="recipe_ingredients")


class Floor(Base):
    __tablename__ = "floor"

    id = Column(Integer, primary_key=True)
    item_sku = Column(Text, ForeignKey("item.sku"), nullable=False)
    quantity = Column(Integer, nullable=False)
    dropped_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    item = relationship("Item", back_populates="floor_drops")



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
