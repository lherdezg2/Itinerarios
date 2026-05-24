from django.test import TestCase

from itinerary_service.application.itinerary_edit_rules import (
    ItineraryEditNotAllowedError,
    ensure_itinerary_editable,
)
from itinerary_service.domain.itinerary import ItineraryStatus


class ItineraryEditRulesTestCase(TestCase):
    def test_pending_is_editable(self):
        ensure_itinerary_editable(ItineraryStatus.PENDIENTE)

    def test_in_progress_is_editable(self):
        ensure_itinerary_editable(ItineraryStatus.EN_CURSO)

    def test_completed_is_not_editable(self):
        with self.assertRaises(ItineraryEditNotAllowedError):
            ensure_itinerary_editable(ItineraryStatus.COMPLETADO)
