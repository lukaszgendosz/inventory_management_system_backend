from app.configs.exception.exception import CannotDelete, NotFoundError, AlreadyExistsError
from app.repositories import DepartmentRepository
from app.models import Department
from app.schemes import DepartmentCreateScheme, DepartmentUpdateScheme, GenericFilterParams


class DepartmentService:

    def __init__(self, department_repository: DepartmentRepository) -> None:
        self._repository: DepartmentRepository = department_repository

    def get_departments(self, params: GenericFilterParams) -> list[Department]:
        return self._repository.get_paginated_list(params)

    def get_department_by_id(self, department_id: int) -> Department:
        department = self._repository.get_by_id(department_id)
        if not department:
            raise NotFoundError("Department not found.")
        return department

    def create_department(self, request: DepartmentCreateScheme) -> Department:
        department = Department(**request.model_dump())
        return self._repository.save(department)

    def update_department(self, department_id: int, request: DepartmentUpdateScheme):
        department = self.get_department_by_id(department_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(department, key, value)
        return self._repository.save(department)

    def delete_department_by_id(self, department_id: int) -> None:
        department = self.get_department_by_id(department_id)
        if department.users:
            raise CannotDelete("Cannot delete department with users assigned.")
        return self._repository.delete(department)
