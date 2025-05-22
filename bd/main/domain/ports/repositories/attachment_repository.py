from abc import ABC, abstractmethod

from main.domain.model.statistics import Statistics


class AttachmentRepository(ABC):
    @abstractmethod
    def get_attachment_statistics(self) -> Statistics:
        pass
