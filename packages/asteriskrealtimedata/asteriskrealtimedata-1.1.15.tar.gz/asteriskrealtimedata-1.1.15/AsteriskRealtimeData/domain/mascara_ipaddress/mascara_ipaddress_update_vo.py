from AsteriskRealtimeData.domain.update_vo import UpdateVo
from dataclasses import dataclass
from typing import Any


@dataclass
class MascaraIpaddressUpdateVo(UpdateVo):
    ipaddress: str
    lastconnection: Any = None
    _update_keys: str = "ipaddress"
