from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent/".env",
                                      env_file_encoding='utf-8',
                                      extra='allow')
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    
    
    def generate_db_uri(self) -> None:
        self.DATABASE_URI = PostgresDsn.build(
            scheme= 'postgresql+asyncpg',
            username = self.POSTGRES_USER,
            password = self.POSTGRES_PASSWORD,
            host = self.POSTGRES_SERVER,
            port= self.POSTGRES_PORT,
            path = self.POSTGRES_DB
        ).unicode_string()
            
    
config = Settings(_env_file=Path(__file__).parent.parent/".env")
config.generate_db_uri()
