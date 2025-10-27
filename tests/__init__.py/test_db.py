import pytest
import datetime
from sqlalchemy.orm import Session


@pytest.fixture
def session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


def test_models_init(session: Session):
    from models import Client, Order
    # Test that we can create instances of the models
    client = Client(acronym="ABC", full_name="Alpha Beta Corp")
    order = Order(
        symbol="AAPL",
        quantity=100,
        state="received",
        received_time=datetime.datetime.now(),
        processed_time=None,
        filled_time=None,
        client="ABC",
        received_event_id=1,
    )
    session.add(client)
    session.add(order)
    session.commit()

    retrieved_client = session.query(Client).filter_by(acronym="ABC").first()
    retrieved_order = session.query(Order).filter_by(symbol="AAPL").first()

    assert retrieved_client is not None
    assert retrieved_order is not None
    assert retrieved_client.full_name == "Alpha Beta Corp"
    assert retrieved_order.quantity == 100

def test_order_client_relationship(session: Session):
    from models import Client, Order
    client = Client(acronym="XYZ", full_name="Xylon Zeta Yards")
    order = Order(
        symbol="GOOG",
        quantity=50,
        state="received",
        received_time=datetime.datetime.now(),
        processed_time=None,
        filled_time=None,
        client="XYZ",
        received_event_id=2,
    )
    session.add(client)
    session.add(order)
    session.commit()

    retrieved_order = session.query(Order).filter_by(symbol="GOOG").first()
    assert retrieved_order is not None
    assert retrieved_order.client == "XYZ"

def test_order_unique_received_event_id(session: Session):
    from models import Order
    order1 = Order(
        symbol="MSFT",
        quantity=200,
        state="received",
        received_time=datetime.datetime.now(),
        processed_time=None,
        filled_time=None,
        client="DEF",
        received_event_id=3,
    )
    order2 = Order(
        symbol="TSLA",
        quantity=150,
        state="received",
        received_time=datetime.datetime.now(),
        processed_time=None,
        filled_time=None,
        client="DEF",
        received_event_id=3,  # Duplicate ID
    )
    session.add(order1)
    session.commit()
    session.add(order2)
    with pytest.raises(Exception):
        session.commit()
        session.rollback()

def test_client_primary_key(session: Session):
    from models import Client
    client1 = Client(acronym="LMN", full_name="Lumen Networks")
    client2 = Client(acronym="LMN", full_name="Lunar Missions")  # Duplicate acronym
    session.add(client1)
    session.commit()
    session.add(client2)
    with pytest.raises(Exception):
        session.commit()
        session.rollback()


def test_order_state_update(session: Session):
    from models import Order
    order = Order(
        symbol="NFLX",
        quantity=75,
        state="received",
        received_time=datetime.datetime.now(),
        processed_time=None,
        filled_time=None,
        client="GHI",
        received_event_id=4,
    )
    session.add(order)
    session.commit()

    # Update order state
    order.state = "processed"
    order.processed_time = datetime.datetime.now()
    session.commit()

    retrieved_order = session.query(Order).filter_by(symbol="NFLX").first()
    assert retrieved_order is not None
    assert retrieved_order.state == "processed"
    assert retrieved_order.processed_time is not None


def test_order_filled(session: Session):
    from models import Order
    order = Order(
        symbol="AMZN",
        quantity=120,
        state="processed",
        received_time=datetime.datetime.now() - datetime.timedelta(hours=1),
        processed_time=datetime.datetime.now() - datetime.timedelta(minutes=30),
        filled_time=None,
        client="JKL",
        received_event_id=5,
    )
    session.add(order)
    session.commit()

    # Update order to filled
    order.state = "filled"
    order.filled_time = datetime.datetime.now()
    session.commit()

    retrieved_order = session.query(Order).filter_by(symbol="AMZN").first()
    assert retrieved_order is not None
    assert retrieved_order.state == "filled"
    assert retrieved_order.filled_time is not None

