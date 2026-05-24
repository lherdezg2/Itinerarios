from abc import ABC, abstractmethod

from itinerary_service.domain.itinerary import Itinerary


class ItineraryCommandPort(ABC):
    @abstractmethod
    def create_itinerary(
        self,
        itinerary_id: str,
        origin_airport_id: str,
        destination_airport_id: str,
        travel_date_iso: str,
        start_time_iso: str,
        end_time_iso: str,
    ) -> Itinerary:
        raise NotImplementedError

    @abstractmethod
    def list_itineraries(self) -> list[Itinerary]:
        raise NotImplementedError

    @abstractmethod
    def get_itinerary_by_id(self, itinerary_id: str) -> Itinerary | None:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, itinerary_id: str, new_status: str) -> Itinerary:
        raise NotImplementedError

    @abstractmethod
    def delete_itinerary(self, itinerary_id: str) -> None:
        raise NotImplementedError
