from typing import Any
from dataclasses import dataclass
from AsteriskRealtimeData.domain.search_by_criteria_vo import SearchByCriteriaVo


@dataclass
class QueueMemberSearchCriteriaVoV1(SearchByCriteriaVo):
    peer: Any = None
    actual_status: Any = None
    last_status_code: Any = None
    membername: Any = None
