from dataclasses import dataclass
from datetime import date, time
from enum import Enum


class ItineraryStatus(str, Enum):
    """Estados permitidos (HU-B3). Solo se asigna Pendiente al crear en esta versión."""

    PENDIENTE = "Pendiente"
    EN_CURSO = "En curso"
    COMPLETADO = "Completado"
    CANCELADO = "Cancelado"


@dataclass(frozen=True)
class Itinerary:
    itinerary_id: str
    origin_airport_id: str
    destination_airport_id: str
    travel_date: date
    start_time: time
    end_time: time
    status: ItineraryStatus


def new_itinerary_pending(
    itinerary_id: str,
    origin_airport_id: str,
    destination_airport_id: str,
    travel_date: date,
    start_time: time,
    end_time: time,
) -> Itinerary:
    """Asigna el estado inicial en el dominio (HU-B3)."""
    return Itinerary(
        itinerary_id=itinerary_id,
        origin_airport_id=origin_airport_id,
        destination_airport_id=destination_airport_id,
        travel_date=travel_date,
        start_time=start_time,
        end_time=end_time,
        status=ItineraryStatus.PENDIENTE,
    )
