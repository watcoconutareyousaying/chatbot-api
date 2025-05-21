from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import EmailSchema, OTPVerifySchema
from app.models.user import User
from app.db.session import get_db
from app.services.helpers import generate_otp, otp_expiration_time
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/request-otp")
def request_otp(data: EmailSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        user = User(email=data.email)
        db.add(user)
        db.commit()
        db.refresh(user)

    otp = generate_otp()
    user.otp_code = otp
    user.otp_expiry = otp_expiration_time()
    db.commit()

    print(f"Send this OTP to {user.email}: {otp}")
    return {"message": "OTP sent to your email."}


@router.post("/verify-otp")
def verify_otp(data: OTPVerifySchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    if user.otp_code != data.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP."
        )

    if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired.")

    user.otp_code = None
    user.otp_expiry = None
    db.commit()

    return {"message": "OTP verified, user logged in successfully."}
