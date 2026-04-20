import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from itinerary_service.adapters.outbound.airport_client.static_airport_validation_adapter import (
    StaticAirportValidationAdapter,
)
from itinerary_service.adapters.outbound.db.in_memory_itinerary_repository import (
    InMemoryItineraryRepository,
)
from itinerary_service.application.use_cases.itinerary_service import ItineraryService

_repository = InMemoryItineraryRepository()
_airport_validation = StaticAirportValidationAdapter()
itinerary_service = ItineraryService(_repository, _airport_validation)


@require_POST
def create_itinerary(request):
    try:
        body = json.loads(request.body)
        itinerary = itinerary_service.create_itinerary(
            itinerary_id=body["itinerary_id"],
            origin_airport_id=body["origin_airport_id"],
            destination_airport_id=body["destination_airport_id"],
            start_date_iso=body["start_date"],
            end_date_iso=body["end_date"],
        )
        return JsonResponse(
            {
                "itinerary_id": itinerary.itinerary_id,
                "origin_airport_id": itinerary.origin_airport_id,
                "destination_airport_id": itinerary.destination_airport_id,
                "start_date": itinerary.start_date.isoformat(),
                "end_date": itinerary.end_date.isoformat(),
            },
            status=201,
        )
    except (KeyError, ValueError, json.JSONDecodeError) as error:
        return JsonResponse({"detail": str(error)}, status=400)


@require_GET
def list_itineraries(request):
    items = itinerary_service.list_itineraries()
    payload = [
        {
            "itinerary_id": item.itinerary_id,
            "origin_airport_id": item.origin_airport_id,
            "destination_airport_id": item.destination_airport_id,
            "start_date": item.start_date.isoformat(),
            "end_date": item.end_date.isoformat(),
        }
        for item in items
    ]
    return JsonResponse(payload, safe=False)
