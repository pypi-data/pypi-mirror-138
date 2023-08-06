from dataclasses import dataclass
from datetime import datetime


@dataclass
class LastStatusVo:
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

    def as_dict(self):
        return {
            "peer": self.peer,
            "peer_ipaddress": self.peer_ipaddress,
            "member_name": self.member_name,
            "agent_name": self.agent_name,
            "member_status_code": self.member_status_code,
            "member_status_description": self.member_status_description,
            "member_status_datetime": self.member_status_datetime,
            "member_is_paused": self.member_is_paused,
            "member_pause_reason_code": self.member_pause_reason_code,
            "member_pause_reason_description": self.member_pause_reason_description,
            "member_pause_datetime": self.member_pause_datetime,
            "phone_status_code": self.phone_status_code,
            "phone_status_description": self.phone_status_description,
            "phone_status_datetime": self.phone_status_datetime,
            "call_origin_number": self.call_origin_number,
            "call_destination_number": self.call_destination_number,
            "call_origin_channel": self.call_origin_channel,
            "call_destination_channel": self.call_destination_channel,
            "call_linked_id": self.call_linked_id,
            "call_status": self.call_status,
            "call_initial_datetime": self.call_initial_datetime,
            "call_bridge_datetime": self.call_bridge_datetime,
            "call_hangup_datetime": self.call_hangup_datetime,
            "call_dial_status": self.call_dial_status,
            "queue_call_is_from_queue": self.queue_call_is_from_queue,
            "queue_call_queue": self.queue_call_queue,
            "queue_call_holdtime": self.queue_call_holdtime,
            "queue_call_talktime": self.queue_call_talktime,
            "queue_call_ringtime": self.queue_call_ringtime,
        }
