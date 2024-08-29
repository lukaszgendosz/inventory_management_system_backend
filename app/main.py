from fastapi import FastAPI
import os

from app.routers import router
from app.configs.containers import Application
from app.configs.exception.error_handler import init_error_handler

container = Application()
app = FastAPI(title="Inventory Management System")
app.container = container
init_error_handler(app)

app.include_router(router)