from dataclasses import dataclass
from datetime import datetime
from AsteriskRealtimeData.domain.entity import Entity


@dataclass
class LastStatus(Entity):
    peer: str = ""
    peer_ipaddress: str = ""
    member_name: str = ""
    agent_name: str = ""
    member_status_code: str = ""
    member_status_description: str = ""
    member_status_datetime: datetime = datetime.now()
    member_is_paused: bool = False
    member_pause_reason_code: str = ""
    member_pause_reason_description: str = ""
    member_pause_datetime: datetime = datetime.now()
    phone_status_code: str = ""
    phone_status_description: str = ""
    phone_status_datetime: datetime = datetime.now()
    call_origin_number: str = ""
    call_destination_number: str = ""
    call_origin_channel: str = ""
    call_destination_channel: str = ""
    call_linked_id: str = ""
    call_status: str = ""
    call_initial_datetime: datetime = datetime.now()
    call_bridge_datetime: datetime = datetime.now()
    call_hangup_datetime: datetime = datetime.now()
    call_dial_status: str = ""
    queue_call_is_from_queue: bool = False
    queue_call_queue: str = ""
    queue_call_holdtime: int = 0
    queue_call_talktime: int = 0
    queue_call_ringtime: int = 0

    def get_peer(self) -> str:
        return self.peer

    def get_peer_ipaddress(self) -> str:
        return self.peer_ipaddress

    def get_member_name(self) -> str:
        return self.member_name

    def get_agent_name(self) -> str:
        return self.agent_name

    def get_member_status_code(self) -> str:
        return self.member_status_code

    def get_member_status_description(self) -> str:
        return self.member_status_description

    def get_member_status_datetime(self) -> datetime:
        return self.member_status_datetime

    def get_member_is_paused(self) -> bool:
        return self.member_is_paused

    def get_member_pause_reason_code(self) -> str:
        return self.member_pause_reason_code

    def get_member_pause_reason_description(self) -> str:
        return self.member_pause_reason_description

    def get_member_pause_datetime(self) -> datetime:
        return self.member_pause_datetime

    def get_phone_status_code(self) -> str:
        return self.phone_status_code

    def get_phone_status_description(self) -> str:
        return self.phone_status_description

    def get_phone_status_datetime(self) -> datetime:
        return self.phone_status_datetime

    def get_call_origin_number(self) -> str:
        return self.call_origin_number

    def get_call_destination_number(self) -> str:
        return self.call_destination_number

    def get_call_origin_channel(self) -> str:
        return self.call_origin_channel

    def get_call_destination_channel(self) -> str:
        return self.call_destination_channel

    def get_call_linked_id(self) -> str:
        return self.call_linked_id

    def get_call_status(self) -> str:
        return self.call_status

    def get_call_initial_datetime(self) -> datetime:
        return self.call_initial_datetime

    def get_call_bridge_datetime(self) -> datetime:
        return self.call_bridge_datetime

    def get_call_hangup_datetime(self) -> datetime:
        return self.call_hangup_datetime

    def get_call_dial_status(self) -> str:
        return self.call_dial_status

    def get_queue_call_is_from_queue(self) -> bool:
        return self.queue_call_is_from_queue

    def get_queue_call_queue(self) -> str:
        return self.queue_call_queue

    def get_queue_call_holdtime(self) -> int:
        return self.queue_call_holdtime

    def get_queue_call_talktime(self) -> int:
        return self.queue_call_talktime

    def get_queue_call_ringtime(self) -> int:
        return self.queue_call_ringtime

    def as_dict(self):
        return self.__repr__()

    def __repr__(self):
        return {
            "id": self.get_id(),
            "peer": self.get_peer(),
            "peer_ipaddress": self.get_peer_ipaddress(),
            "member_name": self.get_member_name(),
            "agent_name": self.get_agent_name(),
            "member_status_code": self.get_member_status_code(),
            "member_status_description": self.get_member_status_description(),
            "member_status_datetime": self.get_member_status_datetime(),
            "member_is_paused": self.get_member_is_paused(),
            "member_pause_reason_code": self.get_member_pause_reason_code(),
            "member_pause_reason_description": self.get_member_pause_reason_description(),
            "member_pause_datetime": self.get_member_pause_datetime(),
            "phone_status_code": self.get_phone_status_code(),
            "phone_status_description": self.get_phone_status_description(),
            "phone_status_datetime": self.get_phone_status_datetime(),
            "call_origin_number": self.get_call_origin_number(),
            "call_destination_number": self.get_call_destination_number(),
            "call_origin_channel": self.get_call_origin_channel(),
            "call_destination_channel": self.get_call_destination_channel(),
            "call_linked_id": self.get_call_linked_id(),
            "call_status": self.get_call_status(),
            "call_initial_datetime": self.get_call_initial_datetime(),
            "call_bridge_datetime": self.get_call_bridge_datetime(),
            "call_hangup_datetime": self.get_call_hangup_datetime(),
            "call_dial_status": self.get_call_dial_status(),
            "queue_call_is_from_queue": self.get_queue_call_is_from_queue(),
            "queue_call_queue": self.get_queue_call_queue(),
            "queue_call_holdtime": self.get_queue_call_holdtime(),
            "queue_call_talktime": self.get_queue_call_talktime(),
            "queue_call_ringtime": self.get_queue_call_ringtime(),
        }
