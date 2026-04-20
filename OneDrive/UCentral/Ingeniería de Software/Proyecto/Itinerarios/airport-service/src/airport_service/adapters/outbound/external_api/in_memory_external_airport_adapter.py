from airport_service.application.ports.outbound.external_airport_port import ExternalAirportPort
from airport_service.domain.airport import Airport


class InMemoryExternalAirportAdapter(ExternalAirportPort):
    # Datos de ejemplo para el MVP mientras se integra la API externa real.
    _airports = [
        Airport(airport_id="BOG", name="El Dorado", city="Bogota"),
        Airport(airport_id="MDE", name="Jose Maria Cordova", city="Rionegro"),
        Airport(airport_id="CTG", name="Rafael Nunez", city="Cartagena"),
    ]

    def fetch_airport_by_id(self, airport_id: str) -> Airport | None:
        for airport in self._airports:
            if airport.airport_id == airport_id.upper():
                return airport
        return None

    def search_airports(self, term: str) -> list[Airport]:
        normalized = term.lower()
        return [
            airport
            for airport in self._airports
            if normalized in airport.name.lower() or normalized in airport.city.lower()
        ]
