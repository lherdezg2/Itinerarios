import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from itinerary_service.adapters.inbound.rest.status_mapping import status_to_api
from itinerary_service.adapters.inbound.rest.validators import normalize_itinerary_id
from itinerary_service.adapters.outbound.airport_client.http_airport_validation_adapter import (
    HttpAirportValidationAdapter,
)
from itinerary_service.adapters.outbound.db.django_itinerary_repository import (
    DjangoItineraryRepository,
)
from itinerary_service.application.exceptions import (
    ItineraryNotFoundError,
    UpstreamAirportServiceError,
)
from itinerary_service.application.use_cases.itinerary_service import ItineraryService
from itinerary_service.domain.itinerary import Itinerary
from itinerary_service.domain.status_transitions import InvalidStatusTransitionError

logger = logging.getLogger(__name__)

_airport_validation = HttpAirportValidationAdapter(settings.AIRPORT_SERVICE_BASE_URL)
_repository = DjangoItineraryRepository()
itinerary_service = ItineraryService(_repository, _airport_validation)


def _itinerary_to_json(item: Itinerary) -> dict[str, str]:
    """Adaptador REST: dominio -> JSON (HU-C1/C2/C3)."""
    travel_date = item.travel_date.isoformat()
    return {
        "itinerary_id": item.itinerary_id,
        "origin_airport_id": item.origin_airport_id,
        "destination_airport_id": item.destination_airport_id,
        "start_date": travel_date,
        "end_date": travel_date,
        "start_time": item.start_time.strftime("%H:%M:%S"),
        "end_time": item.end_time.strftime("%H:%M:%S"),
        "status": status_to_api(item.status),
    }


def _parse_itinerary_id_or_response(itinerary_id: str) -> tuple[str | None, Response | None]:
    try:
        cleaned = normalize_itinerary_id(itinerary_id)
    except ValueError as error:
        return None, Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
    if cleaned is None:
        return None, Response(
            {"detail": "itinerary_id invalido."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return cleaned, None


class ItineraryListCreateApiView(APIView):
    """GET /api/itineraries/ — listar (HU-C1). POST — crear (HU-B1)."""

    def get(self, request):
        items = itinerary_service.list_itineraries()
        return Response([_itinerary_to_json(item) for item in items], status=status.HTTP_200_OK)

    def post(self, request):
        body = request.data
        try:
            itinerary = itinerary_service.create_itinerary(
                itinerary_id=body["itinerary_id"],
                origin_airport_id=body["origin_airport_id"],
                destination_airport_id=body["destination_airport_id"],
                travel_date_iso=body["travel_date"],
                start_time_iso=body["start_time"],
                end_time_iso=body["end_time"],
            )
            return Response(
                {
                    "message": "Itinerario creado correctamente",
                    "itinerary_id": itinerary.itinerary_id,
                    "status": status_to_api(itinerary.status),
                },
                status=status.HTTP_201_CREATED,
            )
        except UpstreamAirportServiceError as error:
            return Response({"detail": str(error)}, status=status.HTTP_502_BAD_GATEWAY)
        except (KeyError, ValueError) as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)


class ItineraryDetailApiView(APIView):
    """GET /api/itineraries/{itinerary_id}/ — consulta por ID (HU-C2)."""

    def get(self, request, itinerary_id: str):
        cleaned, error_response = _parse_itinerary_id_or_response(itinerary_id)
        if error_response is not None:
            return error_response

        logger.info("Consultando itinerario %s", cleaned)
        itinerary = itinerary_service.get_itinerary_by_id(cleaned)
        if itinerary is None:
            return Response(
                {"detail": "Itinerario no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(_itinerary_to_json(itinerary), status=status.HTTP_200_OK)


class ItineraryStatusUpdateApiView(APIView):
    """PATCH /api/itineraries/{itinerary_id}/status/ — cambio de estado (HU-C3)."""

    def patch(self, request, itinerary_id: str):
        cleaned, error_response = _parse_itinerary_id_or_response(itinerary_id)
        if error_response is not None:
            return error_response

        logger.info("Actualizando estado del itinerario %s", cleaned)
        try:
            new_status = request.data.get("status")
            itinerary = itinerary_service.update_status(cleaned, new_status)
            return Response(_itinerary_to_json(itinerary), status=status.HTTP_200_OK)
        except ItineraryNotFoundError as error:
            return Response({"detail": str(error)}, status=status.HTTP_404_NOT_FOUND)
        except (InvalidStatusTransitionError, ValueError) as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
