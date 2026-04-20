from airport_service.application.ports.inbound.airport_query_port import AirportQueryPort
from airport_service.application.ports.outbound.external_airport_port import (
    ExternalAirportPort,
)
from airport_service.domain.airport import Airport


class AirportQueryService(AirportQueryPort):
    def __init__(self, external_port: ExternalAirportPort) -> None:
        self._external_port = external_port

    def get_airport_by_id(self, airport_id: str) -> Airport | None:
        return self._external_port.fetch_airport_by_id(airport_id)

    def search_airports(self, term: str) -> list[Airport]:
        if not term:
            return []
        return self._external_port.search_airports(term)
