from datetime import date

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
        start_date_iso: str,
        end_date_iso: str,
    ) -> Itinerary:
        self._validate_airports(origin_airport_id, destination_airport_id)
        start_date = date.fromisoformat(start_date_iso)
        end_date = date.fromisoformat(end_date_iso)

        if start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha fin")

        itinerary = Itinerary(
            itinerary_id=itinerary_id,
            origin_airport_id=origin_airport_id.upper(),
            destination_airport_id=destination_airport_id.upper(),
            start_date=start_date,
            end_date=end_date,
        )
        self._itinerary_repository.save(itinerary)
        return itinerary

    def list_itineraries(self) -> list[Itinerary]:
        return self._itinerary_repository.list_all()

    def _validate_airports(self, origin_airport_id: str, destination_airport_id: str) -> None:
        if not self._airport_validation.airport_exists(origin_airport_id):
            raise ValueError("Aeropuerto de origen no valido")
        if not self._airport_validation.airport_exists(destination_airport_id):
            raise ValueError("Aeropuerto de destino no valido")
