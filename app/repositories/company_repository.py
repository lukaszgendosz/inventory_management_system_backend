from app.repositories.base_repository import BaseRepository
from app.models import Company

class CompanyRepository(BaseRepository):
    
    def get_all(self) -> list[Company]:
        with self.session_factory() as session:
            return session.query(Company).all()
        
    def get_by_id(self, company_id: int) -> Company:
        with self.session_factory() as session:
            department = session.query(Company).filter(Company.id == company_id).first()
            return department
        
    