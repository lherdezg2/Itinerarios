from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from django.test import TestCase

from itinerary_service.domain.itinerary import ItineraryStatus
from itinerary_service.domain.status_from_schedule import COLOMBIA_TZ, compute_itinerary_status


class StatusFromScheduleTestCase(TestCase):
    def test_before_start_is_pending(self) -> None:
        travel_date = date(2026, 6, 15)
        now = datetime(2026, 6, 15, 7, 30, tzinfo=COLOMBIA_TZ)
        status = compute_itinerary_status(
            travel_date,
            time(8, 0),
            time(10, 0),
            now=now,
        )
        self.assertEqual(status, ItineraryStatus.PENDIENTE)

    def test_between_start_and_end_is_in_progress(self) -> None:
        travel_date = date(2026, 6, 15)
        now = datetime(2026, 6, 15, 9, 0, tzinfo=COLOMBIA_TZ)
        status = compute_itinerary_status(
            travel_date,
            time(8, 0),
            time(10, 0),
            now=now,
        )
        self.assertEqual(status, ItineraryStatus.EN_CURSO)

    def test_at_end_time_is_still_in_progress(self) -> None:
        travel_date = date(2026, 6, 15)
        now = datetime(2026, 6, 15, 10, 0, tzinfo=COLOMBIA_TZ)
        status = compute_itinerary_status(
            travel_date,
            time(8, 0),
            time(10, 0),
            now=now,
        )
        self.assertEqual(status, ItineraryStatus.EN_CURSO)

    def test_after_end_is_completed(self) -> None:
        travel_date = date(2026, 6, 15)
        now = datetime(2026, 6, 15, 10, 1, tzinfo=COLOMBIA_TZ)
        status = compute_itinerary_status(
            travel_date,
            time(8, 0),
            time(10, 0),
            now=now,
        )
        self.assertEqual(status, ItineraryStatus.COMPLETADO)
