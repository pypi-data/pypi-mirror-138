from AsteriskRealtimeData.domain.update_vo import UpdateVo
from dataclasses import dataclass
from typing import Any


@dataclass
class QueueMemberUpdateVoV1(UpdateVo):
    peer: str
    actual_status: Any = None
    last_status_code: Any = None
    membername: Any = None
    _update_keys: str = "peer"
