from datetime import date, time

from itinerary_service.application.ports.inbound.itinerary_command_port import (
    ItineraryCommandPort,
)
from itinerary_service.application.ports.outbound.airport_validation_port import (
    AirportValidationPort,
)
from itinerary_service.application.ports.outbound.itinerary_repository_port import (
    ItineraryRepositoryPort,
)
from itinerary_service.domain.itinerary import Itinerary


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
        self._validate_airports(origin_airport_id, destination_airport_id)
        travel_date = date.fromisoformat(travel_date_iso)
        start_time = time.fromisoformat(start_time_iso)
        end_time = time.fromisoformat(end_time_iso)

        itinerary = Itinerary(
            itinerary_id=itinerary_id.strip(),
            origin_airport_id=origin_airport_id.strip().upper(),
            destination_airport_id=destination_airport_id.strip().upper(),
            travel_date=travel_date,
            start_time=start_time,
            end_time=end_time,
        )
        self._itinerary_repository.save(itinerary)
        return itinerary

    def list_itineraries(self) -> list[Itinerary]:
        return self._itinerary_repository.list_all()

    def _validate_airports(self, origin_airport_id: str, destination_airport_id: str) -> None:
        if not self._airport_validation.airport_exists(origin_airport_id):
            raise ValueError("El aeropuerto de origen no existe segun el Airport Service.")
        if not self._airport_validation.airport_exists(destination_airport_id):
            raise ValueError("El aeropuerto de destino no existe segun el Airport Service.")
