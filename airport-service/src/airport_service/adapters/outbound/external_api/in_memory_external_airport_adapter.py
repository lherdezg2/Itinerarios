from airport_service.application.ports.outbound.external_airport_port import ExternalAirportPort
from airport_service.domain.airport import Airport
from airport_service.domain.search_text import normalize_search_text


class InMemoryExternalAirportAdapter(ExternalAirportPort):
    # Datos de ejemplo para el MVP mientras se integra la API externa real.
    _airports = [
        Airport(
            airport_id="BOG",
            name="El Dorado",
            city="Bogota",
            latitude=4.70159,
            longitude=-74.1469,
        ),
        Airport(
            airport_id="MDE",
            name="Jose Maria Cordova",
            city="Rionegro",
            latitude=6.16454,
            longitude=-75.4231,
        ),
        Airport(
            airport_id="CTG",
            name="Rafael Nunez",
            city="Cartagena",
            latitude=10.4424,
            longitude=-75.513,
        ),
    ]

    def fetch_airport_by_id(self, airport_id: str) -> Airport | None:
        for airport in self._airports:
            if airport.airport_id == airport_id.upper():
                return airport
        return None

    def search_airports(self, term: str) -> list[Airport]:
        normalized = normalize_search_text(term)
        return [
            airport
            for airport in self._airports
            if normalized in normalize_search_text(airport.name)
            or normalized in normalize_search_text(airport.city)
        ]
