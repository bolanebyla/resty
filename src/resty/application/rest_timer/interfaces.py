from abc import ABC, abstractmethod


class ITimerRepo(ABC):
    @abstractmethod
    def set_rest_end(self):
        ...

    @abstractmethod
    def set_work_start(self):
        ...

    @abstractmethod
    def set_work_end(self):
        ...

    @abstractmethod
    def set_rest_start(self):
        ...

    @abstractmethod
    def is_rest_started(self):
        ...

    @abstractmethod
    def is_work_started(self):
        ...
