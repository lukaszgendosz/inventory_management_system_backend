from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    SupplierCreateScheme,
    SupplierResponseScheme,
    SupplierUpdateScheme,
    SupplierPaginatedResponseScheme,
    GenericFilterParams,
)
from app.services import SupplierService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker

router = APIRouter(tags=["Suppliers"])


@router.get("/suppliers")
@inject
def get_suppliers(
    filter_query: Annotated[GenericFilterParams, Query()],
    supplier_service: SupplierService = Depends(Provide[Application.services.supplier_service]),
    _=Depends(manager_role_checker),
) -> SupplierPaginatedResponseScheme:
    suppliers, total_pages = supplier_service.get_suppliers(
        page=filter_query.page, page_size=filter_query.page_size
    )
    suppliers_schmeas = [SupplierResponseScheme.model_validate(supplier) for supplier in suppliers]
    return SupplierPaginatedResponseScheme(total_pages=total_pages, data=suppliers_schmeas)


@router.get("/suppliers/{supplier_id}")
@inject
def get_suppliers(
    supplier_id: int,
    supplier_service: SupplierService = Depends(Provide[Application.services.supplier_service]),
    _=Depends(manager_role_checker),
) -> SupplierResponseScheme:
    return supplier_service.get_supplier_by_id(supplier_id)


@router.post("/suppliers")
@inject
def create_supplier(
    request: SupplierCreateScheme,
    supplier_service: SupplierService = Depends(Provide[Application.services.supplier_service]),
    _=Depends(manager_role_checker),
) -> SupplierResponseScheme:
    return supplier_service.create_supplier(request)


@router.patch("/suppliers/{supplier_id}")
@inject
def update_supplier(
    supplier_id: int,
    request: SupplierUpdateScheme,
    supplier_service: SupplierService = Depends(Provide[Application.services.supplier_service]),
    _=Depends(manager_role_checker),
) -> SupplierResponseScheme:
    return supplier_service.update_supplier(supplier_id, request)
