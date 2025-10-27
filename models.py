
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import sqlalchemy as sa

class Base(DeclarativeBase):
    pass

class Order(Base):
    __table__ == "orders"

    symbol: Mapped[str]
    quantity: Mapped[int]
    state: Mapped[str]
    received_time: Mapped[datetime.datetime]
    processed_time: Mapped[datetime.datetime | None]
    filled_time: Mapped[datetime.datetime | None]


class Client(Base):
    __table__ == "clients"

    acronym: Mapped[str]
    full_name: Mapped[str]