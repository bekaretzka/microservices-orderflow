from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import TokenResponse, UserRegister, UserLogin, UserRead
from app.database import get_db, engine
from app.models import Base, User
from app.security import hash_password, verify_password, create_access_token


@asynccontextmanager
async def lifespan(_: FastAPI):
    from app.models import User

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: UserRegister,
    db: Session = Depends(get_db)
) -> TokenResponse:
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()

    access_token = create_access_token(user)
    return TokenResponse(access_token=access_token, user=UserRead.model_validate(user))


@app.post("/login", response_model=TokenResponse)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == str(payload.email)))

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user)
    return TokenResponse(access_token=access_token, user=UserRead.model_validate(user))
