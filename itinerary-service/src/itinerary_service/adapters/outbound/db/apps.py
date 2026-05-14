from django.apps import AppConfig


class ItineraryDbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "itinerary_service.adapters.outbound.db"
    label = "itinerary_db"
    verbose_name = "Itinerarios (persistencia)"
