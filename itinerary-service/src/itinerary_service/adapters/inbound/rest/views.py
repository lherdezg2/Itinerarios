import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from itinerary_service.adapters.outbound.airport_client.http_airport_validation_adapter import (
    HttpAirportValidationAdapter,
)
from itinerary_service.adapters.outbound.db.django_itinerary_repository import (
    DjangoItineraryRepository,
)
from itinerary_service.application.exceptions import UpstreamAirportServiceError
from itinerary_service.application.use_cases.itinerary_service import ItineraryService

_airport_validation = HttpAirportValidationAdapter(settings.AIRPORT_SERVICE_BASE_URL)
_repository = DjangoItineraryRepository()
itinerary_service = ItineraryService(_repository, _airport_validation)


@require_POST
def create_itinerary(request):
    try:
        body = json.loads(request.body)
        itinerary = itinerary_service.create_itinerary(
            itinerary_id=body["itinerary_id"],
            origin_airport_id=body["origin_airport_id"],
            destination_airport_id=body["destination_airport_id"],
            travel_date_iso=body["travel_date"],
            start_time_iso=body["start_time"],
            end_time_iso=body["end_time"],
        )
        return JsonResponse(
            {
                "message": "Itinerario creado correctamente",
                "itinerary_id": itinerary.itinerary_id,
            },
            status=201,
        )
    except UpstreamAirportServiceError as error:
        return JsonResponse({"detail": str(error)}, status=502)
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
            "travel_date": item.travel_date.isoformat(),
            "start_time": item.start_time.strftime("%H:%M"),
            "end_time": item.end_time.strftime("%H:%M"),
        }
        for item in items
    ]
    return JsonResponse(payload, safe=False)
