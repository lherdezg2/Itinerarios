from django.http import JsonResponse
from django.views.decorators.http import require_GET

from airport_service.adapters.outbound.external_api.api_colombia_airport_adapter import (
    ApiColombiaAirportAdapter,
)
from airport_service.application.exceptions import ExternalAirportServiceError
from airport_service.application.use_cases.airport_query_service import AirportQueryService

airport_query_service = AirportQueryService(ApiColombiaAirportAdapter())


@require_GET
def search_airports(request):
    term = request.GET.get("q", "").strip()
    try:
        airports = airport_query_service.search_airports(term)
    except ExternalAirportServiceError as error:
        return JsonResponse({"detail": str(error)}, status=502)

    payload = [
        {
            "id": a.airport_id,
            "name": a.name,
            "city": a.city,
            "latitude": a.latitude,
            "longitude": a.longitude,
        }
        for a in airports
    ]
    return JsonResponse(payload, safe=False)


@require_GET
def get_airport_by_id(request, airport_id: str):
    try:
        airport = airport_query_service.get_airport_by_id(airport_id)
    except ExternalAirportServiceError as error:
        return JsonResponse({"detail": str(error)}, status=502)

    if airport is None:
        return JsonResponse({"detail": "Aeropuerto no encontrado"}, status=404)

    return JsonResponse(
        {
            "id": airport.airport_id,
            "name": airport.name,
            "city": airport.city,
            "latitude": airport.latitude,
            "longitude": airport.longitude,
        },
        status=200,
    )
