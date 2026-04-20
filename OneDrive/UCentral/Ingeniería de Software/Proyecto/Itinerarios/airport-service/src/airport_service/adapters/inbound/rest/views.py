from django.http import JsonResponse
from django.views.decorators.http import require_GET

from airport_service.adapters.outbound.external_api.in_memory_external_airport_adapter import (
    InMemoryExternalAirportAdapter,
)
from airport_service.application.use_cases.airport_query_service import AirportQueryService

airport_query_service = AirportQueryService(InMemoryExternalAirportAdapter())


@require_GET
def search_airports(request):
    term = request.GET.get("q", "").strip()
    airports = airport_query_service.search_airports(term)
    payload = [
        {"id": a.airport_id, "name": a.name, "city": a.city}
        for a in airports
    ]
    return JsonResponse(payload, safe=False)


@require_GET
def get_airport_by_id(request, airport_id: str):
    airport = airport_query_service.get_airport_by_id(airport_id)
    if airport is None:
        return JsonResponse({"detail": "Aeropuerto no encontrado"}, status=404)

    return JsonResponse(
        {"id": airport.airport_id, "name": airport.name, "city": airport.city},
        status=200,
    )
