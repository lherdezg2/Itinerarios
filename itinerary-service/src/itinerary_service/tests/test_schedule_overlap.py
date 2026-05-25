from datetime import date, time
from django.test import TestCase
from itinerary_service.domain.schedule_overlap import same_day_time_intervals_overlap

class ItineraryOverlapTestCase(TestCase):
    def test_overlap_detected(self):
        travel_day = date(2026, 5, 15)
        start_a = time(8, 0)
        end_a = time(10, 0)
        start_b = time(9, 0)
        end_b = time(11, 0)

        result = same_day_time_intervals_overlap(
            travel_day,
            start_a,
            end_a,
            travel_day,
            start_b,
            end_b,
        )
        self.assertTrue(result)

class ItineraryNoOverlapTestCase(TestCase):
    def test_no_overlap_at_adjacent_boundaries(self):
        day = date(2026, 5, 15)
        start_a = time(8, 0)
        end_a = time(10, 0)
        start_b = time(10, 0)
        end_b = time(12, 0)
        result = same_day_time_intervals_overlap(
            day,
            start_a,
            end_a,
            day,
            start_b,
            end_b,
        )

        self.assertFalse(result)
