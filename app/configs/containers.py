from dependency_injector import containers, providers
from app.services.user import UserService
from app.repositories.user_repository import UserRepository
from app.services.auth import AuthService
from app.database import Database
from app.configs.config import settings

class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Database, db_url=config.DATABASE_URI)

class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()
    
    user_repository = providers.Factory(
        UserRepository,
        session_factory=gateways.db.provided.session,
    )

class Services(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
    )
    
    auth_service = providers.Factory(
        AuthService,
        user_service = user_service
    )
    
class Application(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.routers.v1.users",
                 "app.routers.auth"]
    )
    
    config = providers.Configuration()
    json_settings = settings.model_dump()
    config.from_dict(json_settings)
    
    gateways = providers.Container(
        Gateways,
        config=config,
    )

    repositories = providers.Container(
        Repositories,
        config=config,
        gateways=gateways,
    )
    
    services = providers.Container(
        Services,
        config=config,
        repositories=repositories,
    )