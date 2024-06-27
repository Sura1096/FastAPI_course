from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from ..db.database import Base


class ToDo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)

