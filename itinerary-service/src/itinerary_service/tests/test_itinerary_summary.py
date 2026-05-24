import unittest
from datetime import date, time
from decimal import Decimal

from itinerary_service.application.ports.outbound.airport_validation_port import (
    AirportValidationPort,
)
from itinerary_service.application.ports.outbound.itinerary_repository_port import (
    ItineraryRepositoryPort,
)
from itinerary_service.application.use_cases.itinerary_service import ItineraryService
from itinerary_service.domain.itinerary import Itinerary, ItineraryStatus, new_itinerary_pending
from itinerary_service.adapters.outbound.db.in_memory_itinerary_repository import (
    InMemoryItineraryRepository,
)


class FakeAirportValidation(AirportValidationPort):
    def airport_exists(self, airport_id: str) -> bool:
        return True


def _itinerary(
    itinerary_id: str,
    status: ItineraryStatus = ItineraryStatus.PENDIENTE,
    value: Decimal = Decimal("0"),
) -> Itinerary:
    return Itinerary(
        itinerary_id=itinerary_id,
        origin_airport_id="BOG",
        destination_airport_id="MDE",
        travel_date=date(2026, 5, 20),
        start_time=time(8, 0),
        end_time=time(10, 0),
        status=status,
        value=value,
    )


class ItinerarySummaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryItineraryRepository()
        self.service = ItineraryService(self.repository, FakeAirportValidation())

    def test_empty_summary_returns_zeros(self) -> None:
        summary = self.service.get_itinerary_summary()
        self.assertEqual(summary.total_itineraries, 0)
        self.assertEqual(summary.total_value, Decimal("0"))
        self.assertEqual(
            summary.count_by_status,
            {"PENDING": 0, "IN_PROGRESS": 0, "COMPLETED": 0},
        )

    def test_summary_aggregates_count_and_value(self) -> None:
        self.repository.save(
            _itinerary("IT-1", ItineraryStatus.PENDIENTE, Decimal("100000"))
        )
        self.repository.save(
            _itinerary("IT-2", ItineraryStatus.EN_CURSO, Decimal("200000"))
        )
        self.repository.save(
            _itinerary("IT-3", ItineraryStatus.COMPLETADO, Decimal("300000"))
        )

        summary = self.service.get_itinerary_summary()
        self.assertEqual(summary.total_itineraries, 3)
        self.assertEqual(summary.total_value, Decimal("600000"))
        self.assertEqual(summary.count_by_status["PENDING"], 1)
        self.assertEqual(summary.count_by_status["IN_PROGRESS"], 1)
        self.assertEqual(summary.count_by_status["COMPLETED"], 1)
