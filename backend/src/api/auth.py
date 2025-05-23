from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.services.auth_service import (
    authenticate_user, 
    create_access_token, 
    create_user, 
    get_current_user
)
from src.services.schemas import UserCreate, UserResponse, TokenResponse

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """
    Register a new user
    """
    try:
        created_user = await create_user(user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/token", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Generate JWT token for authentication
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@auth_router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    """
    Get current user's information
    """
    return current_user
