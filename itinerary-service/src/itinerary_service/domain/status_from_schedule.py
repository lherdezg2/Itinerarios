from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from itinerary_service.domain.itinerary import ItineraryStatus

COLOMBIA_TZ = ZoneInfo("America/Bogota")


def compute_itinerary_status(
    travel_date: date,
    start_time: time,
    end_time: time,
    now: datetime | None = None,
) -> ItineraryStatus:
    """
    Calcula el estado segun la fecha y ventana horaria del viaje (America/Bogota).

  - Pendiente: antes de la hora de inicio
  - En curso: entre inicio y fin (inclusive)
  - Completado: despues de la hora de fin
    """
    reference = now if now is not None else datetime.now(COLOMBIA_TZ)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=COLOMBIA_TZ)

    start_dt = datetime.combine(travel_date, start_time, tzinfo=COLOMBIA_TZ)
    end_dt = datetime.combine(travel_date, end_time, tzinfo=COLOMBIA_TZ)

    if reference < start_dt:
        return ItineraryStatus.PENDIENTE
    if reference <= end_dt:
        return ItineraryStatus.EN_CURSO
    return ItineraryStatus.COMPLETADO
