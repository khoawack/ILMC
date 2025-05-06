from fastapi import FastAPI
from app.api import action 

app = FastAPI()

# Register your route(s)
app.include_router(action.router)
