from sqlalchemy import Column, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(Text, nullable=False)        
    item_name = Column(Text, nullable=False)   
    favorite = Column(Boolean, default=False) 
    amount = Column(Integer, default=0)       