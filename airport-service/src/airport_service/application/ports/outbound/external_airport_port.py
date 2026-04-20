from abc import ABC, abstractmethod

from airport_service.domain.airport import Airport


class ExternalAirportPort(ABC):
    @abstractmethod
    def fetch_airport_by_id(self, airport_id: str) -> Airport | None:
        raise NotImplementedError

    @abstractmethod
    def search_airports(self, term: str) -> list[Airport]:
        raise NotImplementedError
