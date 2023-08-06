from antidote import service
from AsteriskRealtimeData.infrastructure.repositories.mongo.mongo_repository import (
    MongoRespository,
)


@service(singleton=True)
class LastStatusRepository(MongoRespository):
    __tablename__: str = "last_status"
