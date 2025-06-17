from abc import ABC, abstractmethod
from typing import Optional

from . import entities, enums


class IRestTimerRepo(ABC):

    @abstractmethod
    def create(
        self,
        status: enums.RestTimerStatuses,
    ) -> entities.RestTimer:
        ...

    @abstractmethod
    def get(self) -> Optional[entities.RestTimer]:
        ...

    @abstractmethod
    def save_and_flash(
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
