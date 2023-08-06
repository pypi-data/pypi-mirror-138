from AsteriskRealtimeData.domain.entity import Entity
from dataclasses import dataclass


@dataclass
class QueueMemberV1(Entity):
    peer: str
    actual_status: str
    last_status_code: str
    membername: str

    def get_peer(self) -> str:
        return self.peer

    def get_actual_status(self) -> str:
        return self.actual_status

    def get_last_status_code(self) -> str:
        return self.last_status_code

    def get_membername(self) -> str:
        return self.membername

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "id": self.get_id(),
            "peer": self.get_peer(),
            "actual_status": self.get_actual_status(),
            "last_status_code": self.get_last_status_code(),
            "membername": self.get_membername(),
        }
