from typing import List
from antidote import inject, Provide

from AsteriskRealtimeData.domain.last_status.last_status_search_criteria_vo import (
    LastStatusSearchCriteriaVo,
)
from AsteriskRealtimeData.domain.last_status.last_status_update_vo import (
    LastStatusUpdateVo,
)
from AsteriskRealtimeData.domain.last_status.last_status import LastStatus
from AsteriskRealtimeData.domain.last_status.last_status_vo import LastStatusVo

from AsteriskRealtimeData.application.last_status_repository import LastStatusRepository


class LastStatusService:
    @inject
    def create_last_status(
        self, last_status_vo: LastStatusVo, repository: Provide[LastStatusRepository]
    ) -> LastStatusVo:

        # is_queue_member = mascara_ipaddress.ipaddress == queue_member_vo.ipaddress

        last_status = LastStatus(
            peer=last_status_vo.peer,
            peer_ipaddress=last_status_vo.peer_ipaddress,
            member_name=last_status_vo.member_name,
            agent_name=last_status_vo.agent_name,
            member_status_code=last_status_vo.member_status_code,
            member_status_description=last_status_vo.member_status_description,
            member_status_datetime=last_status_vo.member_status_datetime,
            member_is_paused=last_status_vo.member_is_paused,
            member_pause_reason_code=last_status_vo.member_pause_reason_code,
            member_pause_reason_description=last_status_vo.member_pause_reason_description,
            member_pause_datetime=last_status_vo.member_pause_datetime,
            phone_status_code=last_status_vo.phone_status_code,
            phone_status_description=last_status_vo.phone_status_description,
            phone_status_datetime=last_status_vo.phone_status_datetime,
            call_origin_number=last_status_vo.call_origin_number,
            call_destination_number=last_status_vo.call_destination_number,
            call_origin_channel=last_status_vo.call_origin_channel,
            call_destination_channel=last_status_vo.call_destination_channel,
            call_linked_id=last_status_vo.call_linked_id,
            call_status=last_status_vo.call_status,
            call_initial_datetime=last_status_vo.call_initial_datetime,
            call_bridge_datetime=last_status_vo.call_bridge_datetime,
            call_hangup_datetime=last_status_vo.call_hangup_datetime,
            call_dial_status=last_status_vo.call_dial_status,
            queue_call_is_from_queue=last_status_vo.queue_call_is_from_queue,
            queue_call_queue=last_status_vo.queue_call_queue,
            queue_call_holdtime=last_status_vo.queue_call_holdtime,
            queue_call_talktime=last_status_vo.queue_call_talktime,
            queue_call_ringtime=last_status_vo.queue_call_ringtime,
        )
        repository.save(last_status, {"peer": last_status_vo.peer})

        return LastStatusVo(
            peer=last_status_vo.peer,
            peer_ipaddress=last_status_vo.peer_ipaddress,
            member_name=last_status_vo.member_name,
            agent_name=last_status_vo.agent_name,
            member_status_code=last_status_vo.member_status_code,
            member_status_description=last_status_vo.member_status_description,
            member_status_datetime=last_status_vo.member_status_datetime,
            member_is_paused=last_status_vo.member_is_paused,
            member_pause_reason_code=last_status_vo.member_pause_reason_code,
            member_pause_reason_description=last_status_vo.member_pause_reason_description,
            member_pause_datetime=last_status_vo.member_pause_datetime,
            phone_status_code=last_status_vo.phone_status_code,
            phone_status_description=last_status_vo.phone_status_description,
            phone_status_datetime=last_status_vo.phone_status_datetime,
            call_origin_number=last_status_vo.call_origin_number,
            call_destination_number=last_status_vo.call_destination_number,
            call_origin_channel=last_status_vo.call_origin_channel,
            call_destination_channel=last_status_vo.call_destination_channel,
            call_linked_id=last_status_vo.call_linked_id,
            call_status=last_status_vo.call_status,
            call_initial_datetime=last_status_vo.call_initial_datetime,
            call_bridge_datetime=last_status_vo.call_bridge_datetime,
            call_hangup_datetime=last_status_vo.call_hangup_datetime,
            call_dial_status=last_status_vo.call_dial_status,
            queue_call_is_from_queue=last_status_vo.queue_call_is_from_queue,
            queue_call_queue=last_status_vo.queue_call_queue,
            queue_call_holdtime=last_status_vo.queue_call_holdtime,
            queue_call_talktime=last_status_vo.queue_call_talktime,
            queue_call_ringtime=last_status_vo.queue_call_ringtime,
        )

    @inject
    def update_last_status(
        self,
        last_status_update_vo: LastStatusUpdateVo,
        repository: Provide[LastStatusRepository],
    ) -> LastStatusVo:
        repository.update(last_status_update_vo)

        last_status_dict = repository.get_by_criteria(
            last_status_update_vo.get_key_field()
        )

        return LastStatusVo(
            peer=last_status_dict["peer"],
            peer_ipaddress=last_status_dict["peer_ipaddress"],
            member_name=last_status_dict["member_name"],
            agent_name=last_status_dict["agent_name"],
            member_status_code=last_status_dict["member_status_code"],
            member_status_description=last_status_dict["member_status_description"],
            member_status_datetime=last_status_dict["member_status_datetime"],
            member_is_paused=last_status_dict["member_is_paused"],
            member_pause_reason_code=last_status_dict["member_pause_reason_code"],
            member_pause_reason_description=last_status_dict[
                "member_pause_reason_description"
            ],
            member_pause_datetime=last_status_dict["member_pause_datetime"],
            phone_status_code=last_status_dict["phone_status_code"],
            phone_status_description=last_status_dict["phone_status_description"],
            phone_status_datetime=last_status_dict["phone_status_datetime"],
            call_origin_number=last_status_dict["call_origin_number"],
            call_destination_number=last_status_dict["call_destination_number"],
            call_origin_channel=last_status_dict["call_origin_channel"],
            call_destination_channel=last_status_dict["call_destination_channel"],
            call_linked_id=last_status_dict["call_linked_id"],
            call_status=last_status_dict["call_status"],
            call_initial_datetime=last_status_dict["call_initial_datetime"],
            call_bridge_datetime=last_status_dict["call_bridge_datetime"],
            call_hangup_datetime=last_status_dict["call_hangup_datetime"],
            call_dial_status=last_status_dict["call_dial_status"],
            queue_call_is_from_queue=last_status_dict["queue_call_is_from_queue"],
            queue_call_queue=last_status_dict["queue_call_queue"],
            queue_call_holdtime=last_status_dict["queue_call_holdtime"],
            queue_call_talktime=last_status_dict["queue_call_talktime"],
            queue_call_ringtime=last_status_dict["queue_call_ringtime"],
        )

    @inject()
    def last_status_list(
        self, repository: Provide[LastStatusRepository]
    ) -> List[LastStatusVo]:
        result: list = []
        for document in repository.list():
            result.append(
                LastStatusVo(
                    peer=document["peer"],
                    peer_ipaddress=document["peer_ipaddress"],
                    member_name=document["member_name"],
                    agent_name=document["agent_name"],
                    member_status_code=document["member_status_code"],
                    member_status_description=document["member_status_description"],
                    member_status_datetime=document["member_status_datetime"],
                    member_is_paused=document["member_is_paused"],
                    member_pause_reason_code=document["member_pause_reason_code"],
                    member_pause_reason_description=document[
                        "member_pause_reason_description"
                    ],
                    member_pause_datetime=document["member_pause_datetime"],
                    phone_status_code=document["phone_status_code"],
                    phone_status_description=document["phone_status_description"],
                    phone_status_datetime=document["phone_status_datetime"],
                    call_origin_number=document["call_origin_number"],
                    call_destination_number=document["call_destination_number"],
                    call_origin_channel=document["call_origin_channel"],
                    call_destination_channel=document["call_destination_channel"],
                    call_linked_id=document["call_linked_id"],
                    call_status=document["call_status"],
                    call_initial_datetime=document["call_initial_datetime"],
                    call_bridge_datetime=document["call_bridge_datetime"],
                    call_hangup_datetime=document["call_hangup_datetime"],
                    call_dial_status=document["call_dial_status"],
                    queue_call_is_from_queue=document["queue_call_is_from_queue"],
                    queue_call_queue=document["queue_call_queue"],
                    queue_call_holdtime=document["queue_call_holdtime"],
                    queue_call_talktime=document["queue_call_talktime"],
                    queue_call_ringtime=document["queue_call_ringtime"],
                )
            )
        return result

    @inject
    def get_last_status(
        self, peer: str, repository: Provide[LastStatusRepository]
    ) -> LastStatusVo:
        last_status = repository.get_by_criteria({"peer": peer})
        return LastStatusVo(
            peer=last_status["peer"],
            peer_ipaddress=last_status["peer_ipaddress"],
            member_name=last_status["member_name"],
            agent_name=last_status["agent_name"],
            member_status_code=last_status["member_status_code"],
            member_status_description=last_status["member_status_description"],
            member_status_datetime=last_status["member_status_datetime"],
            member_is_paused=last_status["member_is_paused"],
            member_pause_reason_code=last_status["member_pause_reason_code"],
            member_pause_reason_description=last_status[
                "member_pause_reason_description"
            ],
            member_pause_datetime=last_status["member_pause_datetime"],
            phone_status_code=last_status["phone_status_code"],
            phone_status_description=last_status["phone_status_description"],
            phone_status_datetime=last_status["phone_status_datetime"],
            call_origin_number=last_status["call_origin_number"],
            call_destination_number=last_status["call_destination_number"],
            call_origin_channel=last_status["call_origin_channel"],
            call_destination_channel=last_status["call_destination_channel"],
            call_linked_id=last_status["call_linked_id"],
            call_status=last_status["call_status"],
            call_initial_datetime=last_status["call_initial_datetime"],
            call_bridge_datetime=last_status["call_bridge_datetime"],
            call_hangup_datetime=last_status["call_hangup_datetime"],
            call_dial_status=last_status["call_dial_status"],
            queue_call_is_from_queue=last_status["queue_call_is_from_queue"],
            queue_call_queue=last_status["queue_call_queue"],
            queue_call_holdtime=last_status["queue_call_holdtime"],
            queue_call_talktime=last_status["queue_call_talktime"],
            queue_call_ringtime=last_status["queue_call_ringtime"],
        )

    @inject
    def get_by_search_criteria(
        self,
        search_criteria: LastStatusSearchCriteriaVo,
        repository: Provide[LastStatusRepository],
    ) -> LastStatusVo:
        last_status = repository.get_by_criteria(search_criteria.as_dict())
        return LastStatusVo(
            peer=last_status["peer"],
            peer_ipaddress=last_status["peer_ipaddress"],
            member_name=last_status["member_name"],
            agent_name=last_status["agent_name"],
            member_status_code=last_status["member_status_code"],
            member_status_description=last_status["member_status_description"],
            member_status_datetime=last_status["member_status_datetime"],
            member_is_paused=last_status["member_is_paused"],
            member_pause_reason_code=last_status["member_pause_reason_code"],
            member_pause_reason_description=last_status[
                "member_pause_reason_description"
            ],
            member_pause_datetime=last_status["member_pause_datetime"],
            phone_status_code=last_status["phone_status_code"],
            phone_status_description=last_status["phone_status_description"],
            phone_status_datetime=last_status["phone_status_datetime"],
            call_origin_number=last_status["call_origin_number"],
            call_destination_number=last_status["call_destination_number"],
            call_origin_channel=last_status["call_origin_channel"],
            call_destination_channel=last_status["call_destination_channel"],
            call_linked_id=last_status["call_linked_id"],
            call_status=last_status["call_status"],
            call_initial_datetime=last_status["call_initial_datetime"],
            call_bridge_datetime=last_status["call_bridge_datetime"],
            call_hangup_datetime=last_status["call_hangup_datetime"],
            call_dial_status=last_status["call_dial_status"],
            queue_call_is_from_queue=last_status["queue_call_is_from_queue"],
            queue_call_queue=last_status["queue_call_queue"],
            queue_call_holdtime=last_status["queue_call_holdtime"],
            queue_call_talktime=last_status["queue_call_talktime"],
            queue_call_ringtime=last_status["queue_call_ringtime"],
        )

    @inject
    def delete_last_status(
        self, peer: str, repository: Provide[LastStatusRepository]
    ) -> None:
        repository.delete_by_criteria({"peer": peer})
