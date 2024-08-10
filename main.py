from fastapi import FastAPI
from routers import users, assets

app = FastAPI(title="Inventory Management System")

app.include_router(users.router)
app.include_router(assets.router)