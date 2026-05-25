from dataclasses import replace
from datetime import date, time
from decimal import Decimal

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
from itinerary_service.application.itinerary_edit_rules import ensure_itinerary_editable
from itinerary_service.application.status_codes import (
    API_STATUS_COMPLETED,
    API_STATUS_IN_PROGRESS,
    API_STATUS_PENDING,
    status_to_api,
)
from itinerary_service.domain.itinerary import Itinerary, new_itinerary_pending
from itinerary_service.domain.itinerary_id import normalize_itinerary_id
from itinerary_service.domain.itinerary_summary import ItinerarySummary
from itinerary_service.domain.schedule_overlap import same_day_time_intervals_overlap
from itinerary_service.domain.status_from_schedule import compute_itinerary_status


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
        travel_value: object,
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
        value = self._parse_value(travel_value)

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
            value=value,
        )
        self._itinerary_repository.save(itinerary)
        return self._apply_computed_status(itinerary)

    def list_itineraries(self) -> list[Itinerary]:
        return [
            self._apply_computed_status(item)
            for item in self._itinerary_repository.list_all()
        ]

    def get_itinerary_by_id(self, itinerary_id: str) -> Itinerary | None:
        cleaned = self._normalize_itinerary_id(itinerary_id)
        if cleaned is None:
            return None
        itinerary = self._itinerary_repository.get_by_itinerary_id(cleaned)
        if itinerary is None:
            return None
        return self._apply_computed_status(itinerary)

    def update_status(self, itinerary_id: str, new_status: str) -> Itinerary:
        cleaned_id = self._normalize_itinerary_id(itinerary_id)
        if cleaned_id is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        itinerary = self._itinerary_repository.get_by_itinerary_id(cleaned_id)
        if itinerary is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        return self._apply_computed_status(itinerary)

    def delete_itinerary(self, itinerary_id: str) -> None:
        cleaned_id = self._normalize_itinerary_id(itinerary_id)
        if cleaned_id is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        itinerary = self._itinerary_repository.get_by_itinerary_id(cleaned_id)
        if itinerary is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        self._itinerary_repository.delete(itinerary)

    def update_itinerary(self, itinerary_id: str, data: dict) -> Itinerary:
        if not isinstance(data, dict):
            raise ValueError("El cuerpo de la solicitud debe ser un objeto JSON.")

        forbidden = {"itinerary_id", "status", "travel_date"}
        if forbidden.intersection(data.keys()):
            raise ValueError("No se permite modificar itinerary_id, status ni travel_date.")

        cleaned_id = self._normalize_itinerary_id(itinerary_id)
        if cleaned_id is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        itinerary = self._itinerary_repository.get_by_itinerary_id(cleaned_id)
        if itinerary is None:
            raise ItineraryNotFoundError("Itinerario no encontrado.")

        itinerary = self._apply_computed_status(itinerary)
        ensure_itinerary_editable(itinerary.status)

        origin = itinerary.origin_airport_id
        if "origin_airport_id" in data:
            origin = (data["origin_airport_id"] or "").strip().upper()
            if not origin:
                raise ValueError("El aeropuerto de origen es obligatorio.")

        destination = itinerary.destination_airport_id
        if "destination_airport_id" in data:
            destination = (data["destination_airport_id"] or "").strip().upper()
            if not destination:
                raise ValueError("El aeropuerto de destino es obligatorio.")

        travel_date = itinerary.travel_date
        if "start_date" in data:
            travel_date = self._parse_date(str(data["start_date"]))
        if "end_date" in data:
            end_date = self._parse_date(str(data["end_date"]))
            if "start_date" in data and end_date != travel_date:
                raise ValueError("start_date y end_date deben coincidir en el MVP.")
            travel_date = end_date

        start_time = itinerary.start_time
        if "start_time" in data:
            start_time = self._parse_time(str(data["start_time"]))

        end_time = itinerary.end_time
        if "end_time" in data:
            end_time = self._parse_time(str(data["end_time"]))

        if end_time <= start_time:
            raise ValueError("La hora final debe ser mayor que la inicial")

        value = itinerary.value
        if "value" in data:
            value = self._parse_value(data["value"])

        self._validate_airports(origin, destination)
        self._ensure_no_overlap(
            travel_date,
            start_time,
            end_time,
            exclude_itinerary_id=cleaned_id,
        )

        updated = replace(
            itinerary,
            origin_airport_id=origin,
            destination_airport_id=destination,
            travel_date=travel_date,
            start_time=start_time,
            end_time=end_time,
            value=value,
        )
        self._itinerary_repository.save(updated)
        return self._apply_computed_status(updated)

    def get_itinerary_summary(self) -> ItinerarySummary:
        itineraries = self.list_itineraries()
        count_by_status = {
            API_STATUS_PENDING: 0,
            API_STATUS_IN_PROGRESS: 0,
            API_STATUS_COMPLETED: 0,
        }
        total_value = Decimal("0")
        for item in itineraries:
            api_status = status_to_api(item.status)
            if api_status in count_by_status:
                count_by_status[api_status] += 1
            total_value += item.value
        return ItinerarySummary(
            total_itineraries=len(itineraries),
            total_value=total_value,
            count_by_status=count_by_status,
        )

    def _apply_computed_status(self, itinerary: Itinerary) -> Itinerary:
        computed = compute_itinerary_status(
            itinerary.travel_date,
            itinerary.start_time,
            itinerary.end_time,
        )
        if itinerary.status != computed:
            updated = replace(itinerary, status=computed)
            self._itinerary_repository.save(updated)
            return updated
        return itinerary

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

    def _parse_value(self, value: object) -> Decimal:
        if value is None:
            raise ValueError("El valor del viaje es obligatorio.")
        raw = str(value).strip()
        if not raw:
            raise ValueError("El valor del viaje es obligatorio.")
        normalized = raw.replace("$", "").replace(" ", "")
        if normalized.count(",") == 1 and normalized.count(".") == 0:
            normalized = normalized.replace(",", ".")
        else:
            normalized = normalized.replace(",", "")
        try:
            parsed = Decimal(normalized)
        except Exception as exc:
            raise ValueError("El valor del viaje debe ser un numero valido.") from exc
        if parsed < 0:
            raise ValueError("El valor del viaje debe ser mayor o igual a cero.")
        return parsed.quantize(Decimal("0.01"))

    def _validate_airports(self, origin_airport_id: str, destination_airport_id: str) -> None:
        if not self._airport_validation.airport_exists(origin_airport_id):
            raise ValueError("El aeropuerto de origen no existe segun el Airport Service.")
        if not self._airport_validation.airport_exists(destination_airport_id):
            raise ValueError("El aeropuerto de destino no existe segun el Airport Service.")

    def _ensure_no_overlap(
        self,
        travel_date: date,
        start_time: time,
        end_time: time,
        exclude_itinerary_id: str | None = None,
    ) -> None:
        for existing in self._itinerary_repository.get_by_date(travel_date):
            if exclude_itinerary_id and existing.itinerary_id == exclude_itinerary_id:
                continue
            if same_day_time_intervals_overlap(
                existing.travel_date,
                existing.start_time,
                existing.end_time,
                travel_date,
                start_time,
                end_time,
            ):
                raise ValueError("El itinerario se solapa con otro existente")
