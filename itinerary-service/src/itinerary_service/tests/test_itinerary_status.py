from datetime import date, time
from django.test import TestCase
from itinerary_service.domain.itinerary import ItineraryStatus, new_itinerary_pending

class ItineraryStatusTestCase(TestCase):
    def test_initial_status_is_pending(self):
        itinerary = new_itinerary_pending(
            itinerary_id="ITI-003",
            origin_airport_id="BOG",
            destination_airport_id="MDE",
            travel_date=date(2026, 5, 20),
            start_time=time(8, 0),
            end_time=time(10, 0),
        )
        self.assertEqual(itinerary.status, ItineraryStatus.PENDIENTE)
        self.assertEqual(itinerary.status.value, "Pendiente")
