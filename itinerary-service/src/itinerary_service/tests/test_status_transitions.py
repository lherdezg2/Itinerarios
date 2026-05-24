from django.test import TestCase

from itinerary_service.application.status_codes import (
    API_STATUS_COMPLETED,
    API_STATUS_IN_PROGRESS,
    API_STATUS_PENDING,
)
from itinerary_service.application.status_transitions import (
    InvalidStatusTransitionError,
    ensure_valid_status_transition,
    is_valid_api_transition,
)
from itinerary_service.domain.itinerary import ItineraryStatus


class StatusTransitionRulesTestCase(TestCase):
    def test_pending_to_in_progress_allowed(self):
        self.assertTrue(is_valid_api_transition(API_STATUS_PENDING, API_STATUS_IN_PROGRESS))

    def test_pending_to_completed_allowed(self):
        self.assertTrue(is_valid_api_transition(API_STATUS_PENDING, API_STATUS_COMPLETED))

    def test_in_progress_to_completed_allowed(self):
        self.assertTrue(is_valid_api_transition(API_STATUS_IN_PROGRESS, API_STATUS_COMPLETED))

    def test_completed_to_pending_not_allowed(self):
        self.assertFalse(is_valid_api_transition(API_STATUS_COMPLETED, API_STATUS_PENDING))

    def test_completed_to_in_progress_raises(self):
        with self.assertRaises(InvalidStatusTransitionError):
            ensure_valid_status_transition(
                ItineraryStatus.COMPLETADO,
                ItineraryStatus.EN_CURSO,
            )
