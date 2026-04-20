from abc import ABC, abstractmethod

from itinerary_service.domain.itinerary import Itinerary


class ItineraryRepositoryPort(ABC):
    @abstractmethod
    def save(self, itinerary: Itinerary) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Itinerary]:
        raise NotImplementedError
