from antidote import service
from AsteriskRealtimeData.infrastructure.repositories.mongo.mongo_repository import (
    MongoRespository,
)


@service(singleton=True)
class AgentRepository(MongoRespository):
    __tablename__: str = "agents"

