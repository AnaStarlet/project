import fastapi
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import get_db, Base, engine
import models, schemas, auth
import secrets
from datetime import datetime, timedelta
from mailhog_service import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])

class VerificationToken(Base):
    __tablename__ = "verification_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)

VerificationToken.__table__.create(bind=engine, checkfirst=True)

@router.post("/register", response_model=schemas.UserResponse)
def register(
        user: schemas.UserCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    existing = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
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
    token_record = VerificationToken(
        token=verify_token,
        email=user.email,
        username=user.username,
        user_id=db_user.id,
        created_at=datetime.utcnow(),
        is_used=False
    )
    db.add(token_record)
    db.commit()

    background_tasks.add_task(
        send_verification_email,
        user.email,
        user.username,
        verify_token
    )

    return db_user

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    token_record = db.query(VerificationToken).filter(
        VerificationToken.token == token,
        VerificationToken.is_used == False
    ).first()

    if not token_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    if datetime.utcnow() - token_record.created_at > timedelta(hours=24):
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(models.User).filter(models.User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    token_record.is_used = True
    db.commit()

    return {"message": "Email confirmed successfully"}

@router.post("/login", response_model=schemas.Token)
def login(
        form_data: fastapi.security.OAuth2PasswordRequestForm = Depends(),
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