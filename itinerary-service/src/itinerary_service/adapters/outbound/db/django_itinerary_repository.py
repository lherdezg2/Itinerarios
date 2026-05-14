from itinerary_service.adapters.outbound.db.models import ItineraryRecord
from itinerary_service.application.ports.outbound.itinerary_repository_port import (
    ItineraryRepositoryPort,
)
from itinerary_service.domain.itinerary import Itinerary


class DjangoItineraryRepository(ItineraryRepositoryPort):
    def save(self, itinerary: Itinerary) -> None:
        ItineraryRecord.objects.update_or_create(
            itinerary_id=itinerary.itinerary_id,
            defaults={
                "origin_airport_id": itinerary.origin_airport_id,
                "destination_airport_id": itinerary.destination_airport_id,
                "travel_date": itinerary.travel_date,
                "start_time": itinerary.start_time,
                "end_time": itinerary.end_time,
            },
        )

    def list_all(self) -> list[Itinerary]:
        rows = ItineraryRecord.objects.all().order_by("itinerary_id")
        return [_to_domain(row) for row in rows]


def _to_domain(row: ItineraryRecord) -> Itinerary:
    return Itinerary(
        itinerary_id=row.itinerary_id,
        origin_airport_id=row.origin_airport_id,
        destination_airport_id=row.destination_airport_id,
        travel_date=row.travel_date,
        start_time=row.start_time,
        end_time=row.end_time,
    )
