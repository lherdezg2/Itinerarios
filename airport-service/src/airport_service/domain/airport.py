from dataclasses import dataclass


@dataclass(frozen=True)
class Airport:
    airport_id: str
    name: str
    city: str
