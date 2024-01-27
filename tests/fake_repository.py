import random

from chatcleaner.domain.model import model
from chatcleaner.domain.ports.repositories.cleaning import CleaningRespositoryInterface


class FakeCleaningRepository(CleaningRespositoryInterface):
    def __init__(self):
        super().__init__()
        self.database = {}

    def _add(self, cleaning: model.Cleaning) -> None:
        id_ = random.randint(10, 100)
        self.database[id_] = cleaning

    def _get(self, id_: str) -> model.Cleaning:
        return self.database.get(id_)

    def _get_by_uuid(self, uuid: str) -> model.Cleaning:
        for val in self.database.values():
            if val.uuid == uuid:
                return val

    def _get_all(self) -> list[model.Cleaning]:
        return list(self.database.values())
