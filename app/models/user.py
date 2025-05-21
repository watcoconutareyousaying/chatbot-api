from sqlalchemy.orm import  Mapped, mapped_column
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    otp_code: Mapped[str | None] = mapped_column(nullable=True)
    otp_expiry: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
