from .base_repository import BaseRepository
from app.models import Location

class LocationRepository(BaseRepository):
    
    def get_all(self) -> list[Location]:
        with self.session_factory() as session:
            return session.query(Location).all()
        
    def get_by_id(self, location_id: int) -> Location:
        with self.session_factory() as session:
            location = session.query(Location).filter(Location.id == location_id).first()
            return location