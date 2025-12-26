from typing import Optional, List

from pydantic import BaseModel, Field
from fastapi_utils.enums import CamelStrEnum



class UserRight(CamelStrEnum):
    ADMIN = "ADMIN"
    CONTRIBUTOR = "CONTRIBUTOR"
    USER = "USER"


class UserBase(BaseModel):
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    rights: List[UserRight] = []
    first_name: Optional[str] = None
    last_name: Optional[str] = None