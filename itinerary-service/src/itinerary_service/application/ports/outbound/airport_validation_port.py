from abc import ABC, abstractmethod


class AirportValidationPort(ABC):
    @abstractmethod
    def airport_exists(self, airport_id: str) -> bool:
        raise NotImplementedError
