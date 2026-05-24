from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ItinerarySummary:
    total_itineraries: int
    total_value: Decimal
    count_by_status: dict[str, int]
