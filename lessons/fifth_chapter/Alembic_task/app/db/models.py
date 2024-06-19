from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column


from ..db.database import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True
    )

    title: Mapped[str]
    price: Mapped[int]
    count: Mapped[int]
    description: Mapped[str]
