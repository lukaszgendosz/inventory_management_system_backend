from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.schemes import DepartmentCreateScheme, DepartmentResponseScheme, DepartmentUpdateScheme
from app.services import DepartmentService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=['Departments'])

@router.get('/departments')
@inject
def get_departments(
    department_service: DepartmentService = Depends(Provide[Application.services.department_service]),
    _ = Depends(manager_role_checker)
    ) -> list[DepartmentResponseScheme]:
    return department_service.get_departments()

@router.get('/departments/{department_id}')
@inject
def get_departments(
    department_id: int,
    department_service: DepartmentService = Depends(Provide[Application.services.department_service]),
    _ = Depends(manager_role_checker)
    ) -> DepartmentResponseScheme:
    return department_service.get_department_by_id(department_id)


@router.post('/departments')
@inject
def create_department(
    request: DepartmentCreateScheme,
    department_service: DepartmentService = Depends(Provide[Application.services.department_service]),
    _ = Depends(admin_role_checker)
    ) -> DepartmentResponseScheme:
    return department_service.create_department(request)

@router.patch('/departments/{department_id}')
@inject
def update_department(
    department_id: int,
    request: DepartmentUpdateScheme,
    department_service: DepartmentService = Depends(Provide[Application.services.department_service]),
    _ = Depends(admin_role_checker)
    ) -> DepartmentResponseScheme:
    return department_service.update_department(department_id,request)