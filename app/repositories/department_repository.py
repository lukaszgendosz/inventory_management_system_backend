from app.repositories.base_repository import BaseRepository
from app.models import Department

class DepartmentRepository(BaseRepository):
    
    def get_all(self) -> list[Department]:
        with self.session_factory() as session:
            return session.query(Department).all()
        
    def get_by_id(self, department_id: int) -> Department:
        with self.session_factory() as session:
            department = session.query(Department).filter(Department.id == department_id).first()
            return department
        
    