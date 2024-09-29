from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    DepartmentCreateScheme,
    DepartmentResponseScheme,
    DepartmentUpdateScheme,
    DepartmentPaginatedResponseScheme,
    GenericFilterParams,
)
from app.services import DepartmentService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=["Departments"])


@router.get("/departments")
@inject
def get_departments(
    filter_query: Annotated[GenericFilterParams, Query()],
    department_service: DepartmentService = Depends(
        Provide[Application.services.department_service]
    ),
    _=Depends(manager_role_checker),
) -> DepartmentPaginatedResponseScheme:
    departments, total_pages = department_service.get_departments(
        page=filter_query.page, page_size=filter_query.page_size
    )
    departments_schmeas = [
        DepartmentResponseScheme.model_validate(department)
        for department in departments
    ]
    return DepartmentPaginatedResponseScheme(
        total_pages=total_pages, data=departments_schmeas
    )


@router.get("/departments/{department_id}")
@inject
def get_departments(
    department_id: int,
    department_service: DepartmentService = Depends(
        Provide[Application.services.department_service]
    ),
    _=Depends(manager_role_checker),
) -> DepartmentResponseScheme:
    return department_service.get_department_by_id(department_id)


@router.post("/departments")
@inject
def create_department(
    request: DepartmentCreateScheme,
    department_service: DepartmentService = Depends(
        Provide[Application.services.department_service]
    ),
    _=Depends(admin_role_checker),
) -> DepartmentResponseScheme:
    return department_service.create_department(request)


@router.patch("/departments/{department_id}")
@inject
def update_department(
    department_id: int,
    request: DepartmentUpdateScheme,
    department_service: DepartmentService = Depends(
        Provide[Application.services.department_service]
    ),
    _=Depends(admin_role_checker),
) -> DepartmentResponseScheme:
    return department_service.update_department(department_id, request)
