from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    SELLER = "seller"
    ADMIN = "admin"
