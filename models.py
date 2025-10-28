
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa

class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    acronym: Mapped[str] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column()

class Order(Base):
    __tablename__ = "orders"

    symbol: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    state: Mapped[str] = mapped_column()
    received_time: Mapped[datetime.datetime] = mapped_column()
    processed_time: Mapped[datetime.datetime | None] = mapped_column()
    filled_time: Mapped[datetime.datetime | None] = mapped_column()
    client: Mapped[str] = mapped_column(sa.ForeignKey(Client.acronym))
    received_event_id: Mapped[int] = mapped_column(primary_key=True)
    filled_quantity: Mapped[int | None] = mapped_column()


class Exchange(Base):
    __tablename__ = "exchanges"

    name: Mapped[str] = mapped_column(primary_key=True)
    full_name: Mapped[str]


class ExchangeEvent(Base):
    __tablename__ = "exchange_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exchange: Mapped[str] = mapped_column(sa.ForeignKey(Exchange.name))
    event_type: Mapped[str]
    event_time: Mapped[datetime.datetime]
    details: Mapped[str | None] = mapped_column()
    timestamp: Mapped[datetime.datetime]

class Symbol(Base):
    __tablename__ = "symbols"

    symbol: Mapped[str] = mapped_column(primary_key=True)
    exchange: Mapped[str] = mapped_column(sa.ForeignKey(Exchange.name))
    primary_listing: Mapped[str]
    description: Mapped[str]
