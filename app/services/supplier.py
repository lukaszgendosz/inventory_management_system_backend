from app.configs.exception.exception import NotFoundError
from app.repositories import SupplierRepository
from app.models import Supplier
from app.schemes import SupplierCreateScheme, SupplierUpdateScheme, GenericFilterParams


class SupplierService:

    def __init__(self, supplier_repository: SupplierRepository) -> None:
        self._repository: SupplierRepository = supplier_repository

    def get_suppliers(self, params: GenericFilterParams) -> list[Supplier]:
        return self._repository.get_paginated_list(params)

    def get_supplier_by_id(self, supplier_id: int) -> Supplier:
        supplier = self._repository.get_by_id(supplier_id)
        if not supplier:
            raise NotFoundError("Supplier not found.")
        return supplier

    def create_supplier(self, request: SupplierCreateScheme) -> Supplier:
        supplier = Supplier(**request.model_dump())
        return self._repository.save(supplier)

    def update_supplier(self, supplier_id: int, request: SupplierUpdateScheme):
        supplier = self.get_supplier_by_id(supplier_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(supplier, key, value)
        return self._repository.save(supplier)

    def delete_supplier_by_id(self, supplier_id: int) -> None:
        supplier = self.get_supplier_by_id(supplier_id)
        return self._repository.delete(supplier)
