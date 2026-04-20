from django.urls import path

from itinerary_service.adapters.inbound.rest.views import create_itinerary, list_itineraries

urlpatterns = [
    path("", create_itinerary, name="create-itinerary"),
    path("list/", list_itineraries, name="list-itineraries"),
]
