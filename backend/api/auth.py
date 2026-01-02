from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from database import get_session
from models import User, UserRole

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(request: LoginRequest, session: Session = Depends(get_session)):
    print(f"🔐 [BACKEND] Login attempt for user: {request.username}")
    statement = select(User).where(User.username == request.username)
    user = session.exec(statement).first()

    # In a real app, use pwd_context.verify(request.password, user.hashed_password)
    # For this prototype, we'll check if password matches hashed_password literally
    # as we will seed it with simple strings for ease of use.
    if not user or user.hashed_password != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "full_name": user.full_name,
        "token": f"mock-token-for-{user.username}",
    }
