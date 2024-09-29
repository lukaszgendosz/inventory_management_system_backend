from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import router
from app.configs.containers import Application
from app.configs.exception.error_handler import init_error_handler

container = Application()
app = FastAPI(title="Inventory Management System")
app.container = container
app.mount("/attachments", StaticFiles(directory="/attachments"), name="uploads")
init_error_handler(app)

app.include_router(router)
