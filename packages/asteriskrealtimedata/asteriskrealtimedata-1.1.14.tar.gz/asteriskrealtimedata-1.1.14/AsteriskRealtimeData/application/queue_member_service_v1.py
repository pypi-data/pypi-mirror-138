from typing import List
from antidote import inject, Provide

from AsteriskRealtimeData.domain.queue_member_v1.queue_member_search_criteria_vo_v1 import (
    QueueMemberSearchCriteriaVoV1,
)
from AsteriskRealtimeData.domain.queue_member_v1.queue_member_update_vo_v1 import (
    QueueMemberUpdateVoV1,
)
from AsteriskRealtimeData.application.queue_member_repository_v1 import (
    QueueMemberRepositoryV1,
)
from AsteriskRealtimeData.domain.queue_member_v1.queue_member_v1 import QueueMemberV1
from AsteriskRealtimeData.domain.queue_member_v1.queue_member_vo_v1 import (
    QueueMemberVoV1,
)


class QueueMemberServiceV1:
    @inject
    def create_queue_member(
        self,
        queue_member_vo: QueueMemberVoV1,
        repository: Provide[QueueMemberRepositoryV1],
    ) -> QueueMemberVoV1:
        queue_member = QueueMemberV1(
            peer=queue_member_vo.peer,
            actual_status=queue_member_vo.actual_status,
            last_status_code=queue_member_vo.last_status_code,
            membername=queue_member_vo.membername,
        )

        repository.save(queue_member, {"peer": queue_member_vo.peer})

        return QueueMemberVoV1(
            peer=queue_member_vo.peer,
            actual_status=queue_member_vo.actual_status,
            last_status_code=queue_member_vo.last_status_code,
            membername=queue_member_vo.membername,
        )

    @inject
    def update_queue_member(
        self,
        queue_member_update_vo: QueueMemberUpdateVoV1,
        repository: Provide[QueueMemberRepositoryV1],
    ) -> QueueMemberVoV1:
        repository.update(queue_member_update_vo)

        queue_member_dict = repository.get_by_criteria(
            queue_member_update_vo.get_key_field()
        )

        return QueueMemberVoV1(
            peer=queue_member_dict["peer"],
            actual_status=queue_member_dict["actual_status"],
            last_status_code=queue_member_dict["last_status_code"],
            membername=queue_member_dict["membername"],
        )

    @inject()
    def queue_member_list(
        self, repository: Provide[QueueMemberRepositoryV1]
    ) -> List[QueueMemberVoV1]:
        result: list = []
        for document in repository.list(
            special_conditions={"membername": {"$exists": True}}
        ):
            result.append(
                QueueMemberVoV1(
                    peer=document["peer"],
                    actual_status=document["actual_status"]
                    if "actual_status" in document
                    else "",
                    last_status_code=document["last_status_code"],
                    membername=document["membername"]
                    if "membername" in document
                    else None,
                )
            )
        return result

    @inject
    def get_queue_member(
        self, peer: str, repository: Provide[QueueMemberRepositoryV1]
    ) -> QueueMemberVoV1:
        queue_member = repository.get_by_criteria({"peer": peer})
        return QueueMemberVoV1(
            peer=queue_member["peer"],
            actual_status=queue_member["actual_status"],
            last_status_code=queue_member["last_status_code"],
            membername=queue_member["membername"],
        )

    @inject
    def get_by_search_criteria(
        self,
        search_criteria: QueueMemberSearchCriteriaVoV1,
        repository: Provide[QueueMemberRepositoryV1],
    ) -> QueueMemberVoV1:
        queue_member = repository.get_by_criteria(search_criteria.as_dict())
        return QueueMemberVoV1(
            peer=queue_member["peer"],
            actual_status=queue_member["actual_status"],
            last_status_code=queue_member["last_status_code"],
            membername=queue_member["membername"],
        )

    @inject
    def delete_queue_member(
        self, peer: str, repository: Provide[QueueMemberRepositoryV1]
    ) -> None:
        repository.delete_by_criteria({"peer": peer})
