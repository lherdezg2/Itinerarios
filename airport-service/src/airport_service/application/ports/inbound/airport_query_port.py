from abc import ABC, abstractmethod

from airport_service.domain.airport import Airport


class AirportQueryPort(ABC):
    @abstractmethod
    def get_airport_by_id(self, airport_id: str) -> Airport | None:
        raise NotImplementedError

    @abstractmethod
    def search_airports(self, term: str) -> list[Airport]:
        raise NotImplementedError
