from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    CompanyCreateScheme,
    CompanyResponseScheme,
    CompanyUpdateScheme,
    CompanyPaginatedResponseScheme,
    GenericFilterParams,
)
from app.services import CompanyService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=["Companies"])


@router.get("/companies")
@inject
def get_companies(
    filter_query: Annotated[GenericFilterParams, Query()],
    company_service: CompanyService = Depends(Provide[Application.services.company_service]),
    _=Depends(manager_role_checker),
) -> CompanyPaginatedResponseScheme:
    companies, total_pages = company_service.get_companies(params=filter_query)
    companies_schmeas = [CompanyResponseScheme.model_validate(company) for company in companies]
    return CompanyPaginatedResponseScheme(total_pages=total_pages, data=companies_schmeas)


@router.get("/companies/{company_id}")
@inject
def get_companies(
    company_id: int,
    company_service: CompanyService = Depends(Provide[Application.services.company_service]),
    _=Depends(manager_role_checker),
) -> CompanyResponseScheme:
    return company_service.get_company_by_id(company_id)


@router.post("/companies")
@inject
def create_company(
    request: CompanyCreateScheme,
    company_service: CompanyService = Depends(Provide[Application.services.company_service]),
    _=Depends(admin_role_checker),
) -> CompanyResponseScheme:
    return company_service.create_company(request)


@router.patch("/companies/{company_id}")
@inject
def update_company(
    company_id: int,
    request: CompanyUpdateScheme,
    company_service: CompanyService = Depends(Provide[Application.services.company_service]),
    _=Depends(admin_role_checker),
) -> CompanyResponseScheme:
    return company_service.update_company(company_id, request)
