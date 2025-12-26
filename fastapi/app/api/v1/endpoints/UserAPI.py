
from fastapi import APIRouter, Depends
from app.core.config import settings

from app.crud.UserDBController import UserDBController
from app.schemas.UserSchema import User, UserRight

router = APIRouter()

@router.get("/users", response_model=List[User])
def read_users(
    skip: int = 0, limit: int = None
) -> Any:
    users = UserDBController().get_multi(skip=skip, limit=limit)
    return users