from typing import Union, List
from fastapi import APIRouter, HTTPException
from app.crud_service.user_service import (
    read_users,
    create_user,
    update_user,
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.model.user_model import User, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=User, status_code=201)
async def create_user_handler(user: User):
    """Обработчик создания пользователя."""
    try:
        return create_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_name}/", response_model=User)
async def update_user_handler(user_name: str, user_update: UserUpdate):
    """Обработчик обновления данных пользователя."""
    try:
        return update_user(user_name, user_update)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Union[List[User], dict])
async def get_users():
    """Возвращает список всех пользователей."""
    return read_users()
