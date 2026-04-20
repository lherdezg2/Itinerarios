from abc import ABC, abstractmethod

from itinerary_service.domain.itinerary import Itinerary


class ItineraryCommandPort(ABC):
    @abstractmethod
    def create_itinerary(
        self,
        itinerary_id: str,
        origin_airport_id: str,
        destination_airport_id: str,
        start_date_iso: str,
        end_date_iso: str,
    ) -> Itinerary:
        raise NotImplementedError

    @abstractmethod
    def list_itineraries(self) -> list[Itinerary]:
        raise NotImplementedError
