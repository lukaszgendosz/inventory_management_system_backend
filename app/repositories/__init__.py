from .user import UserRepository
from .token import TokenRepository
from .department import DepartmentRepository
from .location import LocationRepository
from .company import CompanyRepository
from .asset import AssetRepository
from .model import ModelRepository
from .supplier import SupplierRepository
from .manufacturer import ManufacturerRepository
from .asset_logs import AssetLogsRepository

__all__ = [
    "UserRepository",
    "TokenRepository",
    "DepartmentRepository",
    "LocationRepository",
    "CompanyRepository",
    "AssetRepository",
    "ModelRepository",
    "SupplierRepository",
    "ManufacturerRepository",
    "AssetLogsRepository",
]
