from django.urls import path

from airport_service.adapters.inbound.rest.views import get_airport_by_id, search_airports

urlpatterns = [
    path("search/", search_airports, name="search-airports"),
    path("<str:airport_id>/", get_airport_by_id, name="get-airport-by-id"),
]
