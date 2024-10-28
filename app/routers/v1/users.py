from typing import Annotated

from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    UserCreateScheme,
    UserResponseScheme,
    UserUpdateScheme,
    UserPaginatedResponseScheme,
    UserParamsScheme,
)
from app.services import UserService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=["Users"])


@router.get("/users")
@inject
def get_users(
    filter_query: Annotated[UserParamsScheme, Query()],
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _=Depends(manager_role_checker),
) -> UserPaginatedResponseScheme:
    users, total_pages = user_service.get_users(params=filter_query)
    users_schemas = [UserResponseScheme.model_validate(user) for user in users]
    return UserPaginatedResponseScheme(total_pages=total_pages, data=users_schemas)


@router.get("/users/{user_id}")
@inject
def get_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _=Depends(manager_role_checker),
) -> UserResponseScheme:
    return user_service.get_user_by_id(user_id)


@router.post("/users")
@inject
def create_user(
    request: UserCreateScheme,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    # _ = Depends(admin_role_checker)
) -> UserResponseScheme:
    return user_service.create_user(request)


@router.patch("/users/{user_id}")
@inject
def update_user(
    user_id: int,
    request: UserUpdateScheme,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _=Depends(admin_role_checker),
) -> UserResponseScheme:
    return user_service.update_user(user_id, request)


@router.patch("/users/{user_id}/deactivate")
@inject
def deactivate_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    current_user=Depends(admin_role_checker),
) -> None:
    return user_service.deactivate_user(user_id, current_user)


@router.patch("/users/{user_id}/activate")
@inject
def activate_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _=Depends(admin_role_checker),
) -> None:
    return user_service.activate_user(user_id)
