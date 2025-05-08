from fastapi import FastAPI
from app.api import action, inventory


app = FastAPI()

# Register your route(s)
app.include_router(action.router)
app.include_router(inventory.router)