import abc

from chatcleaner.domain.model import model


class CleaningRespositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, cleaning: model.Cleaning) -> None:
        self._add(cleaning)
        self.seen.add(cleaning)

    def get(self, id_: str) -> model.Cleaning:
        cleaning = self._get(id_)
        if cleaning:
            self.seen.add(cleaning)
        return cleaning

    def get_by_uuid(self, uuid: str) -> model.Cleaning:
        cleaning = self._get_by_uuid(uuid)
        if cleaning:
            self.seen.add(cleaning)
        return cleaning

    def get_all(self) -> list[model.Cleaning]:
        return self._get_all()

    @abc.abstractmethod
    def _add(self, cleaning: model.Cleaning) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id_: str) -> model.Cleaning:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_uuid(self, uuid: str) -> model.Cleaning:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(self) -> list[model.Cleaning]:
        raise NotImplementedError
