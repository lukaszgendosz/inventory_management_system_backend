from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    ModelCreateScheme,
    ModelResponseScheme,
    ModelUpdateScheme,
    ModelPaginatedResponseScheme,
    GenericFilterParams,
)
from app.services import ModelService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=["Models"])


@router.get("/models")
@inject
def get_models(
    filter_query: Annotated[GenericFilterParams, Query()],
    model_service: ModelService = Depends(Provide[Application.services.model_service]),
    _=Depends(manager_role_checker),
) -> ModelPaginatedResponseScheme:
    models, total_pages = model_service.get_models(params=filter_query)
    models_schmeas = [ModelResponseScheme.model_validate(model) for model in models]
    return ModelPaginatedResponseScheme(total_pages=total_pages, data=models_schmeas)


@router.get("/models/{model_id}")
@inject
def get_models(
    model_id: int,
    model_service: ModelService = Depends(Provide[Application.services.model_service]),
    _=Depends(manager_role_checker),
) -> ModelResponseScheme:
    return model_service.get_model_by_id(model_id)


@router.post("/models")
@inject
def create_model(
    request: ModelCreateScheme,
    model_service: ModelService = Depends(Provide[Application.services.model_service]),
    _=Depends(manager_role_checker),
) -> ModelResponseScheme:
    return model_service.create_model(request)


@router.patch("/models/{model_id}")
@inject
def update_model(
    model_id: int,
    request: ModelUpdateScheme,
    model_service: ModelService = Depends(Provide[Application.services.model_service]),
    _=Depends(manager_role_checker),
) -> ModelResponseScheme:
    return model_service.update_model(model_id, request)
