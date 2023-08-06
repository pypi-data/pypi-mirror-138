from dataclasses import dataclass


@dataclass
class QueueMemberVoV1:
    peer: str
    actual_status: str
    last_status_code: str
    membername: str

    def as_dict(self) -> dict:
        return self.__repr__()

    def __repr__(self):
        return {
            "peer": self.peer,
            "actual_status": self.actual_status,
            "last_status_code": self.last_status_code,
            "membername": self.membername,
        }
