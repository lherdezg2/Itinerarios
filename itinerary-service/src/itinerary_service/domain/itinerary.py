from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class Itinerary:
    itinerary_id: str
    origin_airport_id: str
    destination_airport_id: str
    travel_date: date
    start_time: time
    end_time: time
