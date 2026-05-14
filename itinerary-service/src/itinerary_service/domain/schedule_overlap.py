from datetime import date, time


def same_day_time_intervals_overlap(
    day_a: date,
    start_a: time,
    end_a: time,
    day_b: date,
    start_b: time,
    end_b: time,
) -> bool:
    """
    Dos ventanas en el mismo día calendario se solapan si se cruzan
    (solapamiento parcial o total). Límites contiguos (fin == inicio) no cuentan como solape.
    """
    if day_a != day_b:
        return False
    return start_a < end_b and end_a > start_b
