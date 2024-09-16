from collections.abc import Iterable

from fastapi import APIRouter, Depends, UploadFile
from dependency_injector.wiring import inject, Provide

from app.schemes import UserCreateScheme, UserResponseScheme, UserUpdateScheme
from app.services import UserService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=['Users'])

@router.get('/users')
@inject
def get_users(
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _ = Depends(manager_role_checker)
    ) -> list[UserResponseScheme]:
    return user_service.get_users()

@router.get('/users/{user_id}')
@inject
def get_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _ = Depends(manager_role_checker)
    ) -> UserResponseScheme:
    return user_service.get_user_by_id(user_id)


@router.post('/users')
@inject
def create_user(
    request: UserCreateScheme,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    # _ = Depends(admin_role_checker)
    ) -> UserResponseScheme:
    return user_service.create_user(request)

@router.patch('/users/{user_id}')
@inject
def update_user(
    user_id: int,
    request: UserUpdateScheme,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _ = Depends(admin_role_checker)
    ) -> UserResponseScheme:
    return user_service.update_user(user_id,request)

@router.patch('/users/{user_id}/deactivate')
@inject
def deactivate_user(
    user_id: int,
    user_service: UserService = Depends(Provide[Application.services.user_service]),
    _ = Depends(admin_role_checker)
    ) -> None:
    return user_service.deactivate_user(user_id)