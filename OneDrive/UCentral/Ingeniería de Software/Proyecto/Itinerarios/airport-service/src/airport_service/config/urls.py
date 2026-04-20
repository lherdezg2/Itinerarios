from django.urls import include, path

urlpatterns = [
    path("api/airports/", include("airport_service.adapters.inbound.rest.urls")),
]
