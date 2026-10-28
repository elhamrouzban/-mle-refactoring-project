from sqlalchemy import Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class House(Base):
    __tablename__ = "houses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bedrooms: Mapped[int] = mapped_column(Integer)
    bathrooms: Mapped[float] = mapped_column(Float)
    sqft_living: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)