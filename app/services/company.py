from app.configs.exception.exception import NotFoundError, AlreadyExistsError
from app.repositories import CompanyRepository
from app.models import Company
from app.schemes import CompanyCreateScheme, CompanyUpdateScheme, GenericFilterParams


class CompanyService:

    def __init__(self, company_repository: CompanyRepository) -> None:
        self._repository: CompanyRepository = company_repository

    def get_companies(self, params: GenericFilterParams) -> list[Company]:
        return self._repository.get_paginated_list(params=params)

    def get_company_by_id(self, company_id: int) -> Company:
        company = self._repository.get_by_id(company_id)
        if not company:
            raise NotFoundError("Company not found.")
        return company

    def create_company(self, request: CompanyCreateScheme) -> Company:
        company = Company(**request.model_dump())
        return self._repository.save(company)

    def update_company(self, company_id: int, request: CompanyUpdateScheme):
        company = self.get_company_by_id(company_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        return self._repository.save(company)

    def delete_company_by_id(self, company_id: int) -> None:
        company = self.get_company_by_id(company_id)
        return self._repository.delete(company)
