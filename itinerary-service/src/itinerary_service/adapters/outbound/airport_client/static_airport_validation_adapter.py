from itinerary_service.application.ports.outbound.airport_validation_port import (
    AirportValidationPort,
)


class StaticAirportValidationAdapter(AirportValidationPort):
    # Para MVP: evita acoplar reglas de dominio al cliente HTTP real.
    _known_airports = {"BOG", "MDE", "CTG"}

    def airport_exists(self, airport_id: str) -> bool:
        return airport_id.upper() in self._known_airports
