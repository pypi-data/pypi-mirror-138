from typing import List
from AsteriskRealtimeData.domain.queue_member_v1.queue_member_search_criteria_vo_v1 import (
    QueueMemberSearchCriteriaVoV1,
)
from AsteriskRealtimeData.domain.queue_member_v1.queue_member_update_vo_v1 import (
    QueueMemberUpdateVoV1,
)
from AsteriskRealtimeData.domain.queue_member_v1.queue_member_vo_v1 import (
    QueueMemberVoV1,
)
from AsteriskRealtimeData.application.queue_member_service_v1 import (
    QueueMemberServiceV1,
)


class QueueMemberControllerV1:
    def create(self, queue_member_vo: QueueMemberVoV1) -> QueueMemberVoV1:
        return QueueMemberServiceV1().create_queue_member(queue_member_vo)

    def update(self, queue_member_update_vo: QueueMemberUpdateVoV1) -> QueueMemberVoV1:
        return QueueMemberServiceV1().update_queue_member(queue_member_update_vo)

    def get_all(self) -> List[QueueMemberVoV1]:
        queue_members = QueueMemberServiceV1().queue_member_list()
        result: list = []
        for queue_member in queue_members:
            result.append(queue_member)
        return result

    def get_by_peer(self, peer: str) -> QueueMemberVoV1:
        return QueueMemberServiceV1().get_queue_member(peer)

    def get_by_search_criteria(
        self, search_criteria: QueueMemberSearchCriteriaVoV1
    ) -> QueueMemberVoV1:
        return QueueMemberServiceV1().get_by_search_criteria(search_criteria)

    def delete_by_peer(self, peer: str) -> None:
        QueueMemberServiceV1().delete_queue_member(peer)
