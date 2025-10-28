
from models import Base
from sqlalchemy import Engine

class DbEngineService:
    pass

class MarketDataService:
    pass

class ExchangeConnectionService:
    pass

class OrderRoutingService:
    pass

class RecordKeepingService:
    pass


class OrderManagementEngine:

    def __init__(self, engine: Engine):

        self.db_engine = engine


    def start(self):

        with self.db_engine.begin() as conn:
            Base.metadata.create_all(conn)

    def pause(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def shutdown(self):
        pass
