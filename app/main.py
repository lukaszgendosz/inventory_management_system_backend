from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router
from app.configs.containers import Application
from app.configs.exception.error_handler import init_error_handler


def configure_middleware(app_: FastAPI):
    origins = [
        "*",
    ]
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


container = Application()
app = FastAPI(title="Inventory Management System")
app.container = container
init_error_handler(app)

app.include_router(router)
configure_middleware(app)
