import fastapi
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth
from mailhog_service import send_verification_email, send_password_reset_email
import secrets
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

verification_tokens = {}


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


@router.post("/register", response_model=schemas.UserResponse)
def register(
        user: schemas.UserCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    existing = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed = auth.get_password_hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
        is_active=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    verify_token = secrets.token_urlsafe(32)

    verification_tokens[verify_token] = {
        "user_id": db_user.id,
        "email": user.email
    }

    print(f"Token saved: {verify_token}")

    background_tasks.add_task(
        send_verification_email,
        user.email,
        user.username,
        verify_token
    )

    return db_user


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    token_data = verification_tokens.get(token)
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()

    del verification_tokens[token]

    return {"message": "Email confirmed successfully"}


@router.post("/login", response_model=schemas.Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Please verify your email first")

    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/request-password-reset")
def request_password_reset(
        email: str,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = secrets.token_urlsafe(32)

    db_token = models.ResetToken(
        token=reset_token,
        user_id=user.id
    )
    db.add(db_token)
    db.commit()

    print(f"Reset token saved: {reset_token}")

    background_tasks.add_task(
        send_password_reset_email,
        email,
        user.username,
        reset_token
    )

    return {"message": "Password reset email sent"}


@router.post("/reset-password")
def reset_password(
        request_data: ResetPasswordRequest,
        db: Session = Depends(get_db)
):
    db_token = db.query(models.ResetToken).filter(
        models.ResetToken.token == request_data.token
    ).first()

    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if db_token.created_at < datetime.utcnow() - timedelta(hours=1):
        db.delete(db_token)
        db.commit()
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(models.User).filter(models.User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = auth.get_password_hash(request_data.new_password)
    db.delete(db_token)
    db.commit()

    return {"message": "Password reset successfully"}