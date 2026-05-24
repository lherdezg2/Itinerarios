from datetime import date

from itinerary_service.application.ports.outbound.itinerary_repository_port import (
    ItineraryRepositoryPort,
)
from itinerary_service.domain.itinerary import Itinerary


class InMemoryItineraryRepository(ItineraryRepositoryPort):
    def __init__(self) -> None:
        self._items: list[Itinerary] = []

    def save(self, itinerary: Itinerary) -> None:
        self._items = [i for i in self._items if i.itinerary_id != itinerary.itinerary_id]
        self._items.append(itinerary)

    def list_all(self) -> list[Itinerary]:
        return list(self._items)

    def get_by_date(self, travel_date: date) -> list[Itinerary]:
        return [i for i in self._items if i.travel_date == travel_date]

    def get_by_itinerary_id(self, itinerary_id: str) -> Itinerary | None:
        for item in self._items:
            if item.itinerary_id == itinerary_id:
                return item
        return None

    def delete(self, itinerary: Itinerary) -> None:
        self._items = [i for i in self._items if i.itinerary_id != itinerary.itinerary_id]
