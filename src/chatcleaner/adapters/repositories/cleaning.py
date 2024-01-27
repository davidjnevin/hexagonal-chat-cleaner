from chatcleaner.domain.model import model
from chatcleaner.domain.ports.repositories.cleaning import CleaningRespositoryInterface


class CleaningSqlAlchemyRepository(CleaningRespositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, cleaning: model.Cleaning) -> None:
        self.session.add(cleaning)
        self.session.commit()

    def _get(self, id_: str) -> model.Cleaning:
        return self.session.query(model.Cleaning).filter_by(id=id_).first()

    def _get_by_uuid(self, uuid: str) -> model.Cleaning:
        return self.session.query(model.Cleaning).filter_by(uuid=uuid).first()

    def _get_all(self) -> list[model.Cleaning]:
        return self.session.query(model.Cleaning).all()
