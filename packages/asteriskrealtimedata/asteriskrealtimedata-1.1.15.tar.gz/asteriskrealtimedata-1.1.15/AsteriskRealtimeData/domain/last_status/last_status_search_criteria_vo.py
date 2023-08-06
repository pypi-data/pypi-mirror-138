from typing import Any
from dataclasses import dataclass
from AsteriskRealtimeData.domain.search_by_criteria_vo import SearchByCriteriaVo


@dataclass
class LastStatusSearchCriteriaVo(SearchByCriteriaVo):
    peer: Any = None
    peer_ipaddress: Any = None
    member_name: Any = None
    agent_name: Any = None
    member_status_code: Any = None
    member_status_description: Any = None
    member_status_datetime: Any = None
    member_is_paused: Any = None
    member_pause_reason_code: Any = None
    member_pause_reason_description: Any = None
    member_pause_datetime: Any = None
    phone_status_code: Any = None
    phone_status_description: Any = None
    phone_status_datetime: Any = None
    call_origin_number: Any = None
    call_destination_number: Any = None
    call_origin_channel: Any = None
    call_destination_channel: Any = None
    call_linked_id: Any = None
    call_status: Any = None
    call_initial_datetime: Any = None
    call_bridge_datetime: Any = None
    call_hangup_datetime: Any = None
    call_dial_status: Any = None
    queue_call_is_from_queue: Any = None
    queue_call_queue: Any = None
    queue_call_holdtime: Any = None
    queue_call_talktime: Any = None
    queue_call_ringtime: Any = None
