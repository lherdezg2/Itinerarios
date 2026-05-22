from django.urls import path

from itinerary_service.adapters.inbound.rest.views import (
    ItineraryDetailApiView,
    ItineraryListCreateApiView,
)

urlpatterns = [
    path("", ItineraryListCreateApiView.as_view(), name="itineraries"),
    path("list/", ItineraryListCreateApiView.as_view(), name="list-itineraries"),
    path("<str:itinerary_id>/", ItineraryDetailApiView.as_view(), name="itinerary-detail"),
]
