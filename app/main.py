from fastapi import FastAPI
from app.api import action, inventory, admin, craft, user, world


app = FastAPI()

# Register your route(s)
app.include_router(action.router)
app.include_router(inventory.router)
app.include_router(admin.router) 
app.include_router(craft.router)
app.include_router(user.router)   
app.include_router(world.router)