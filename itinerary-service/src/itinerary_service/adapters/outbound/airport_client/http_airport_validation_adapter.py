import requests

from itinerary_service.application.exceptions import UpstreamAirportServiceError
from itinerary_service.application.ports.outbound.airport_validation_port import (
    AirportValidationPort,
)


class HttpAirportValidationAdapter(AirportValidationPort):
    """Consulta existencia de aeropuerto vía Airport Service (GET por IATA)."""

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def airport_exists(self, airport_id: str) -> bool:
        code = airport_id.strip().upper()
        if not code:
            return False
        url = f"{self._base_url}/api/airports/{code}/"
        try:
            response = requests.get(url, timeout=self._timeout)
        except requests.RequestException as error:
            raise UpstreamAirportServiceError("No se pudo contactar el Airport Service.") from error

        if response.status_code == 200:
            return True
        if response.status_code == 404:
            return False
        raise UpstreamAirportServiceError(
            f"Airport Service respondio con estado {response.status_code}."
        )
