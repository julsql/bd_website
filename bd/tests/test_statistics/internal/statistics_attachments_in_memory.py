from abc import ABC

from main.domain.model.statistics import Statistics
from main.domain.ports.repositories.attachment_repository import AttachmentRepository


class StatisticsAttachmentsInMemory(AttachmentRepository, ABC):
    def __init__(self, return_value: Statistics) -> None:
        self.return_value = return_value
        self.get_information_called = False

    def get_attachment_statistics(self) -> Statistics:
        self.get_information_called = True
        return self.return_value
