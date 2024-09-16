from app.configs.exception.exception import NotFoundError, AlreadyExistsError
from app.repositories.company_repository import CompanyRepository
from app.models import Company
from app.schemes import CompanyCreateScheme, CompanyUpdateScheme



class CompanyService:

    def __init__(self, department_repository: CompanyRepository) -> None:
        self._repository: CompanyRepository = department_repository

    def get_companies(self) -> list[Company]:
        return self._repository.get_all()

    def get_department_by_id(self, department_id: int) -> Company:
        department = self._repository.get_by_id(department_id)
        if not department:
            raise NotFoundError("Company not found.")
        return department

    def create_department(self, request: CompanyCreateScheme) -> Company:
        department = Company(**request.model_dump())
        return self._repository.save(department)
    
    def update_department(self, department_id: int, request: CompanyUpdateScheme):
        department = self.get_department_by_id(department_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(department, key, value)
        return self._repository.save(department)

    def delete_department_by_id(self, department_id: int) -> None:
        department = self.get_department_by_id(department_id)
        return self._repository.delete(department)
