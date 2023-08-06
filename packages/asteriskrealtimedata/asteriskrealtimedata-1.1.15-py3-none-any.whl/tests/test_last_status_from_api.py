import unittest
from datetime import datetime
from unittest.mock import MagicMock
from typing import Final

from AsteriskRealtimeData.api import Api
from AsteriskRealtimeData.domain.last_status.last_status_search_criteria_vo import (
    LastStatusSearchCriteriaVo,
)
from AsteriskRealtimeData.domain.last_status.last_status_update_vo import (
    LastStatusUpdateVo,
)
from AsteriskRealtimeData.domain.last_status.last_status_vo import LastStatusVo

from AsteriskRealtimeData.shared.errors.data_not_found_error import DataNotFound


class TestLastStatusFromAPI(unittest.TestCase):
    DATA_NO_FOUND: Final = "Data not found"
    DATETIME_FORMAT: Final = "%Y-%m-%d %H:%M:%S"

    def test_pause_reason(self):
        self.maxDiff = None
        actual_datetime = datetime(2022, 1, 1, 15, 0, 0)
        Api.LastStatus.create(
            LastStatusVo(
                peer="SIP/999",
                peer_ipaddress="10.10.10.10",
                member_name="1000",
                agent_name="Juares",
                member_status_code="1",
                member_status_description="Hablando",
                member_status_datetime=actual_datetime,
                member_is_paused=True,
                member_pause_reason_code="300001",
                member_pause_reason_description="En una llamada",
                member_pause_datetime=actual_datetime,
                phone_status_code="1",
                phone_status_description="Some Status",
                phone_status_datetime=actual_datetime,
                call_origin_number="5551234",
                call_destination_number="SIP/999",
                call_origin_channel="channel_origin",
                call_destination_channel="channel_destination",
                call_linked_id="1232132.12312",
                call_status="some call status",
                call_initial_datetime=actual_datetime,
                call_bridge_datetime=actual_datetime,
                call_hangup_datetime=actual_datetime,
                call_dial_status="RINGING",
                queue_call_is_from_queue=True,
                queue_call_queue="ventas",
                queue_call_holdtime=10,
                queue_call_talktime=11,
                queue_call_ringtime=12,
            )
        )

        Api.LastStatus.create(
            LastStatusVo(
                peer="SIP/998",
                peer_ipaddress="10.10.10.11",
                member_name="1001",
                agent_name="Ely",
            )
        )

        self.assertGreaterEqual(len(Api.LastStatus.get_all()), 2)

        self.assertDictEqual(
            Api.LastStatus.get_by_peer("SIP/999").as_dict(),
            LastStatusVo(
                peer="SIP/999",
                peer_ipaddress="10.10.10.10",
                member_name="1000",
                agent_name="Juares",
                member_status_code="1",
                member_status_description="Hablando",
                member_status_datetime=actual_datetime,
                member_is_paused=True,
                member_pause_reason_code="300001",
                member_pause_reason_description="En una llamada",
                member_pause_datetime=actual_datetime,
                phone_status_code="1",
                phone_status_description="Some Status",
                phone_status_datetime=actual_datetime,
                call_origin_number="5551234",
                call_destination_number="SIP/999",
                call_origin_channel="channel_origin",
                call_destination_channel="channel_destination",
                call_linked_id="1232132.12312",
                call_status="some call status",
                call_initial_datetime=actual_datetime,
                call_bridge_datetime=actual_datetime,
                call_hangup_datetime=actual_datetime,
                call_dial_status="RINGING",
                queue_call_is_from_queue=True,
                queue_call_queue="ventas",
                queue_call_holdtime=10,
                queue_call_talktime=11,
                queue_call_ringtime=12,
            ).as_dict(),
        )

        self.assertDictEqual(
            Api.LastStatus.get_by_peer("SIP/999").as_dict(),
            Api.LastStatus.get_by_search_criteria(
                LastStatusSearchCriteriaVo(call_linked_id="1232132.12312",)
            ).as_dict(),
        )

        Api.LastStatus.update(
            LastStatusUpdateVo(
                peer="SIP/998",
                member_is_paused=True,
                member_pause_reason_code="300001",
                member_pause_reason_description="En una llamada",
            )
        )

        last_status_updated = Api.LastStatus.get_by_peer("SIP/998")
        self.assertEqual(last_status_updated.member_pause_reason_code, "300001")

        with self.assertRaises(DataNotFound) as context:
            Api.LastStatus.update(
                LastStatusUpdateVo(peer="SIP/000", member_is_paused=False)
            )

        with self.assertRaises(DataNotFound) as context:
            Api.LastStatus.delete_by_peer("SIP/111")
        self.assertTrue(self.DATA_NO_FOUND in str(context.exception))

        with self.assertRaises(DataNotFound) as context:
            Api.LastStatus.get_by_peer("SIP/222")

        with self.assertRaises(DataNotFound) as context:
            Api.LastStatus.get_by_search_criteria(
                LastStatusSearchCriteriaVo(member_status_code="asdsadda")
            )
