from abc import ABC, abstractmethod
from datetime import date

from itinerary_service.domain.itinerary import Itinerary


class ItineraryRepositoryPort(ABC):
    @abstractmethod
    def save(self, itinerary: Itinerary) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Itinerary]:
        raise NotImplementedError

    @abstractmethod
    def get_by_date(self, travel_date: date) -> list[Itinerary]:
        raise NotImplementedError

    @abstractmethod
    def get_by_itinerary_id(self, itinerary_id: str) -> Itinerary | None:
        raise NotImplementedError
