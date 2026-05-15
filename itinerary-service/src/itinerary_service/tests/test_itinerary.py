from datetime import date, time

from django.test import TestCase

from itinerary_service.domain.itinerary import ItineraryStatus, new_itinerary_pending


class ItineraryDomainTests(TestCase):
    def test_crear_itinerario_valido_estado_pendiente(self):
        itinerary = new_itinerary_pending(
            itinerary_id="ITI-001",
            origin_airport_id="BOG",
            destination_airport_id="MDE",
            travel_date=date(2026, 5, 12),
            start_time=time(8, 30),
            end_time=time(10, 0),
        )

        self.assertEqual(itinerary.itinerary_id, "ITI-001")
        self.assertEqual(itinerary.origin_airport_id, "BOG")
        self.assertEqual(itinerary.destination_airport_id, "MDE")
        self.assertEqual(itinerary.travel_date, date(2026, 5, 12))
        self.assertEqual(itinerary.start_time, time(8, 30))
        self.assertEqual(itinerary.end_time, time(10, 0))
        self.assertEqual(itinerary.status, ItineraryStatus.PENDIENTE)
        self.assertEqual(itinerary.status.value, "Pendiente")
