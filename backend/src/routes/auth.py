"""Authentication routes."""
import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import create_access_token, get_current_user
from src.database import get_session
from src.models import User
from src.schemas import UserCreate, UserLogin, UserResponse, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """Register a new user."""
    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == user_data.email.lower())
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email.lower(),
        password_hash=hashed_password,
        name=user_data.name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create JWT token
    access_token = create_access_token(user_id=new_user.id, email=new_user.email)

    return TokenResponse(access_token=access_token)


@router.post("/signin", response_model=TokenResponse)
async def signin(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    """Authenticate user and return JWT token."""
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == credentials.email.lower())
    )
    user = result.scalar_one_or_none()

    if user is None or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token
    access_token = create_access_token(user_id=user.id, email=user.email)

    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user),
):
    """Get current authenticated user."""
    return current_user
