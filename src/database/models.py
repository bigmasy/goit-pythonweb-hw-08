from datetime import date
from sqlalchemy import  Integer, String, Date
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(20), index=True)
    email: Mapped[str] = mapped_column(String(50),nullable=False, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    birthday: Mapped[date] = mapped_column(Date)
    additional_data: Mapped[str|None] = mapped_column(String(50))
