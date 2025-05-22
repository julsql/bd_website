from abc import ABC, abstractmethod

from main.domain.model.statistics import Statistics


class StatisticsRepository(ABC):
    @abstractmethod
    def get_database_statistics(self) -> Statistics:
        pass
