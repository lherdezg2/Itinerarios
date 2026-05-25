import requests

from airport_service.application.exceptions import ExternalAirportServiceError
from airport_service.application.ports.outbound.external_airport_port import ExternalAirportPort
from airport_service.domain.airport import Airport
from airport_service.domain.search_text import normalize_search_text


class ApiColombiaAirportAdapter(ExternalAirportPort):
    def __init__(self, base_url: str = "https://api-colombia.com/api/v1", timeout: int = 10) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def fetch_airport_by_id(self, airport_id: str) -> Airport | None:
        normalized_id = airport_id.strip().upper()
        if not normalized_id:
            return None

        airports = self._fetch_airports()
        for airport in airports:
            if airport.airport_id == normalized_id:
                return airport
        return None

    def search_airports(self, term: str) -> list[Airport]:
        normalized = normalize_search_text(term)
        if not normalized:
            return []

        airports = self._fetch_airports()
        return [
            airport
            for airport in airports
            if normalized in normalize_search_text(airport.name)
            or normalized in normalize_search_text(airport.city)
        ]

    def _fetch_airports(self) -> list[Airport]:
        try:
            response = requests.get(
                f"{self._base_url}/Airport",
                timeout=self._timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as error:
            raise ExternalAirportServiceError("Error al consultar API Colombia") from error

        if not isinstance(payload, list):
            raise ExternalAirportServiceError("Respuesta invalida de API Colombia")

        airports: list[Airport] = []
        for item in payload:
            airport = self._map_airport(item)
            if airport is not None:
                airports.append(airport)

        return airports

    def _map_airport(self, item: object) -> Airport | None:
        if not isinstance(item, dict):
            return None

        airport_id = str(item.get("iataCode") or "").strip().upper()
        if not airport_id or airport_id == "N/A":
            return None

        name = str(item.get("name") or "").strip()
        city_data = item.get("city")
        city = ""
        if isinstance(city_data, dict):
            city = str(city_data.get("name") or "").strip()

        # API Colombia etiqueta lat/lon al revés: el valor norte-sur viene en "longitude".
        latitude = self._safe_float(item.get("longitude"))
        longitude = self._safe_float(item.get("latitude"))
        if latitude is None or longitude is None:
            return None

        return Airport(
            airport_id=airport_id,
            name=name,
            city=city,
            latitude=latitude,
            longitude=longitude,
        )

    def _safe_float(self, value: object) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
