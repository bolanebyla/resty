from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from . import entities, enums


class ITimerRepo(ABC):
    @abstractmethod
    def create_rest_timer(
            self,
            status: enums.RestTimerStatuses,
            end_rest_time: Optional[datetime] = None,
            end_work_time: Optional[datetime] = None,
    ) -> entities.RestTimer:
        ...

    @abstractmethod
    def get_rest_timer(self) -> entities.RestTimer:
        ...

    @abstractmethod
    def save_rest_timer(
            self, rest_timer: entities.RestTimer
    ) -> entities.RestTimer:
        ...


class ITimerEvents(ABC):
    @abstractmethod
    def start_rest(self):
        ...

    @abstractmethod
    def start_work(self):
        ...


class ISignal(ABC):
    @abstractmethod
    def emit(self):
        ...
