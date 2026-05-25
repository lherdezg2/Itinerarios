import unittest
from datetime import date
from decimal import Decimal

from itinerary_service.application.ports.outbound.airport_validation_port import (
    AirportValidationPort,
)
from itinerary_service.application.use_cases.itinerary_service import ItineraryService
from itinerary_service.adapters.outbound.db.in_memory_itinerary_repository import (
    InMemoryItineraryRepository,
)


class FakeAirportValidation(AirportValidationPort):
    def airport_exists(self, airport_id: str) -> bool:
        return True


class ItineraryValueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ItineraryService(InMemoryItineraryRepository(), FakeAirportValidation())

    def test_create_itinerary_persists_mandatory_value(self) -> None:
        itinerary = self.service.create_itinerary(
            itinerary_id="ITI-010",
            origin_airport_id="BOG",
            destination_airport_id="MDE",
            travel_date_iso="2026-06-01",
            start_time_iso="08:00",
            end_time_iso="10:00",
            travel_value="350000",
        )

        self.assertEqual(itinerary.value, Decimal("350000.00"))

    def test_create_itinerary_rejects_missing_value(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.service.create_itinerary(
                itinerary_id="ITI-011",
                origin_airport_id="BOG",
                destination_airport_id="MDE",
                travel_date_iso="2026-06-02",
                start_time_iso="08:00",
                end_time_iso="10:00",
                travel_value=None,
            )
        self.assertIn("obligatorio", str(ctx.exception).lower())

    def test_create_itinerary_rejects_negative_value(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            self.service.create_itinerary(
                itinerary_id="ITI-012",
                origin_airport_id="BOG",
                destination_airport_id="MDE",
                travel_date_iso="2026-06-03",
                start_time_iso="08:00",
                end_time_iso="10:00",
                travel_value="-1",
            )
        self.assertIn("mayor o igual a cero", str(ctx.exception).lower())

    def test_update_itinerary_persists_value(self) -> None:
        self.service.create_itinerary(
            itinerary_id="ITI-020",
            origin_airport_id="BOG",
            destination_airport_id="MDE",
            travel_date_iso="2026-06-10",
            start_time_iso="08:00",
            end_time_iso="10:00",
            travel_value="200000",
        )
        updated = self.service.update_itinerary(
            "ITI-020",
            {"value": "275000"},
        )
        self.assertEqual(updated.value, Decimal("275000.00"))
