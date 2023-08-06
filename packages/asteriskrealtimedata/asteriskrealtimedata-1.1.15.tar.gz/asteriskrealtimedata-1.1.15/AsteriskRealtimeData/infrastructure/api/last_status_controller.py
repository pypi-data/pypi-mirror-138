from typing import List
from AsteriskRealtimeData.domain.last_status.last_status_search_criteria_vo import (
    LastStatusSearchCriteriaVo,
)
from AsteriskRealtimeData.domain.last_status.last_status_update_vo import (
    LastStatusUpdateVo,
)
from AsteriskRealtimeData.domain.last_status.last_status_vo import LastStatusVo
from AsteriskRealtimeData.application.last_status_service import LastStatusService


class LastStatusController:
    def create(self, last_status_vo: LastStatusVo) -> LastStatusVo:
        return LastStatusService().create_last_status(last_status_vo)

    def update(self, last_status_update_vo: LastStatusUpdateVo) -> LastStatusVo:
        return LastStatusService().update_last_status(last_status_update_vo)

    def get_all(self) -> List[LastStatusVo]:
        last_status_list = LastStatusService().last_status_list()
        result: list = []
        for last_status in last_status_list:
            result.append(last_status)
        return result

    def get_by_peer(self, peer: str) -> LastStatusVo:
        return LastStatusService().get_last_status(peer)

    def get_by_search_criteria(
        self, search_criteria: LastStatusSearchCriteriaVo
    ) -> LastStatusVo:
        return LastStatusService().get_by_search_criteria(search_criteria)

    def delete_by_peer(self, peer: str) -> None:
        LastStatusService().delete_last_status(peer)
