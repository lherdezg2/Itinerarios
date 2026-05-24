from dataclasses import replace
from datetime import date, time

from itinerary_service.application.exceptions import ItineraryNotFoundError
from itinerary_service.application.ports.inbound.itinerary_command_port import (
    ItineraryCommandPort,
)
from itinerary_service.application.ports.outbound.airport_validation_port import (
    AirportValidationPort,
)
from itinerary_service.application.ports.outbound.itinerary_repository_port import (
    ItineraryRepositoryPort,
)
from itinerary_service.application.status_codes import parse_api_status
from itinerary_service.application.status_transitions import ensure_valid_status_transition
from itinerary_service.domain.itinerary import Itinerary, new_itinerary_pending
from itinerary_service.domain.itinerary_id import normalize_itinerary_id
from itinerary_service.domain.schedule_overlap import same_day_time_intervals_overlap


class ItineraryService(ItineraryCommandPort):
    def __init__(
        self,
        itinerary_repository: ItineraryRepositoryPort,
        airport_validation: AirportValidationPort,
    ) -> None:
        self._itinerary_repository = itinerary_repository
        self._airport_validation = airport_validation

    def create_itinerary(
        self,
        itinerary_id: str,
        origin_airport_id: str,
        destination_airport_id: str,
        travel_date_iso: str,
        start_time_iso: str,
        end_time_iso: str,
    ) -> Itinerary:
        itinerary_id_clean = itinerary_id.strip()
        if not itinerary_id_clean:
            raise ValueError("El identificador del itinerario es obligatorio.")

        origin = (origin_airport_id or "").strip().upper()
        destination = (destination_airport_id or "").strip().upper()
        if not origin:
            raise ValueError("El aeropuerto de origen es obligatorio.")
        if not destination:
            raise ValueError("El aeropuerto de destino es obligatorio.")

        travel_date = self._parse_date(travel_date_iso)
        start_time = self._parse_time(start_time_iso)
        end_time = self._parse_time(end_time_iso)

        if end_time <= start_time:
            raise ValueError("La hora final debe ser mayor que la inicial")

        self._validate_airports(origin, destination)
        self._ensure_no_overlap(travel_date, start_time, end_time)

        itinerary = new_itinerary_pending(
            itinerary_id=itinerary_id_clean,
            origin_airport_id=origin,
            destination_airport_id=destination,
            travel_date=travel_date,
            start_time=start_time,
            end_time=end_time,
        )
        self._itinerary_repository.save(itinerary)
        return itinerary

    def list_itineraries(self) -> list[Itinerary]:
        return self._itinerary_repository.list_all()

    def get_itinerary_by_id(self, itinerary_id: str) -> Itinerary | None:
        cleaned = self._normalize_itinerary_id(itinerary_id)
        if cleaned is None:
            return None
        return self._itinerary_repository.get_by_itinerary_id(cleaned)

    def update_status(self, itinerary_id: str, new_status: str) -> Itinerary:
        cleaned_id = self._normalize_itinerary_id(itinerary_id)
        if cleaned_id is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        itinerary = self._itinerary_repository.get_by_itinerary_id(cleaned_id)
        if itinerary is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        parsed_status = parse_api_status(new_status)
        ensure_valid_status_transition(itinerary.status, parsed_status)
        updated = replace(itinerary, status=parsed_status)
        self._itinerary_repository.save(updated)
        return updated

    def _normalize_itinerary_id(self, itinerary_id: str | None) -> str | None:
        try:
            return normalize_itinerary_id(itinerary_id)
        except ValueError:
            return None

    def _parse_date(self, value: str) -> date:
        raw = (value or "").strip()
        if not raw:
            raise ValueError("La fecha del viaje es obligatoria.")
        return date.fromisoformat(raw)

    def _parse_time(self, value: str) -> time:
        """Acepta 'HH:MM' y 'HH:MM:SS' (y variantes con microsegundos que fromisoformat permita)."""
        v = (value or "").strip()
        if not v:
            raise ValueError("La hora es obligatoria.")
        if len(v) == 5 and v[2] == ":":
            v = v + ":00"
        return time.fromisoformat(v)

    def _validate_airports(self, origin_airport_id: str, destination_airport_id: str) -> None:
        if not self._airport_validation.airport_exists(origin_airport_id):
            raise ValueError("El aeropuerto de origen no existe segun el Airport Service.")
        if not self._airport_validation.airport_exists(destination_airport_id):
            raise ValueError("El aeropuerto de destino no existe segun el Airport Service.")

    def _ensure_no_overlap(self, travel_date: date, start_time: time, end_time: time) -> None:
        for existing in self._itinerary_repository.get_by_date(travel_date):
            if same_day_time_intervals_overlap(
                existing.travel_date,
                existing.start_time,
                existing.end_time,
                travel_date,
                start_time,
                end_time,
            ):
                raise ValueError("El itinerario se solapa con otro existente")
