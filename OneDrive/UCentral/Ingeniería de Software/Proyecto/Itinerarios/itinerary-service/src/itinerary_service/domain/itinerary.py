from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Itinerary:
    itinerary_id: str
    origin_airport_id: str
    destination_airport_id: str
    start_date: date
    end_date: date
