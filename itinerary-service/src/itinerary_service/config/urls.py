from django.urls import include, path

urlpatterns = [
    path("api/itineraries/", include("itinerary_service.adapters.inbound.rest.urls")),
]
