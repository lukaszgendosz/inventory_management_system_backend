from dependency_injector import containers, providers
from app.models import (
    User,
    Token,
    Department,
    Location,
    Company,
    Asset,
    Model,
    Supplier,
    Manufacturer,
    AssetLogs,
)
from app.services import (
    CompanyService,
    UserService,
    AuthService,
    UserService,
    DepartmentService,
    LocationService,
    AssetService,
    ManufacturerService,
    ModelService,
    SupplierService,
    AssetLogsService,
)
from app.repositories import (
    CompanyRepository,
    UserRepository,
    TokenRepository,
    DepartmentRepository,
    LocationRepository,
    AssetRepository,
    ManufacturerRepository,
    ModelRepository,
    SupplierRepository,
    AssetLogsRepository,
)
from app.database import Database
from app.configs.config import settings


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Database, db_url=config.DATABASE_URI)


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    user_repository = providers.Factory(
        UserRepository, session_factory=gateways.db.provided.session, model_class=User
    )

    token_repository = providers.Factory(
        TokenRepository, session_factory=gateways.db.provided.session, model_class=Token
    )

    department_repository = providers.Factory(
        DepartmentRepository,
        session_factory=gateways.db.provided.session,
        model_class=Department,
    )

    location_repository = providers.Factory(
        LocationRepository,
        session_factory=gateways.db.provided.session,
        model_class=Location,
    )

    company_repository = providers.Factory(
        CompanyRepository,
        session_factory=gateways.db.provided.session,
        model_class=Company,
    )

    asset_repository = providers.Factory(
        AssetRepository, session_factory=gateways.db.provided.session, model_class=Asset
    )

    asset_logs_repository = providers.Factory(
        AssetLogsRepository,
        session_factory=gateways.db.provided.session,
        model_class=AssetLogs,
    )

    manufacturer_repository = providers.Factory(
        ManufacturerRepository,
        session_factory=gateways.db.provided.session,
        model_class=Manufacturer,
    )

    model_repository = providers.Factory(
        ModelRepository, session_factory=gateways.db.provided.session, model_class=Model
    )

    supplier_repository = providers.Factory(
        SupplierRepository,
        session_factory=gateways.db.provided.session,
        model_class=Supplier,
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
    )

    auth_service = providers.Factory(AuthService, user_service=user_service)

    department_service = providers.Factory(
        DepartmentService, department_repository=repositories.department_repository
    )

    location_service = providers.Factory(
        LocationService, location_repository=repositories.location_repository
    )

    company_service = providers.Factory(
        CompanyService, company_repository=repositories.company_repository
    )

    asset_logs_service = providers.Factory(
        AssetLogsService, asset_logs_repository=repositories.asset_logs_repository
    )

    asset_service = providers.Factory(
        AssetService,
        asset_repository=repositories.asset_repository,
        user_service=user_service,
        asset_logs_service=asset_logs_service,
    )

    manufacturer_service = providers.Factory(
        ManufacturerService, manufacturer_repository=repositories.manufacturer_repository
    )

    model_service = providers.Factory(ModelService, model_repository=repositories.model_repository)

    supplier_service = providers.Factory(
        SupplierService, supplier_repository=repositories.supplier_repository
    )


class Application(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.routers.auth",
            "app.routers.v1.users",
            "app.routers.v1.assets",
            "app.routers.v1.asset_logs",
            "app.routers.v1.departments",
            "app.routers.v1.locations",
            "app.routers.v1.companies",
            "app.routers.v1.manufacturers",
            "app.routers.v1.models",
            "app.routers.v1.suppliers",
            "app.utils.security",
            "app.utils.dependencies",
        ]
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
