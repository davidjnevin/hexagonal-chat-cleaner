from typing import Any, Callable

from sqlalchemy import Session

from chatcleaner.adapters.repositories.cleaning import CleaningSqlAlchemyRepository
from chatcleaner.domain.ports.unit_of_works.cleaning import CleaningUnitOfWorkInterface


class CleaningSqlAlchemyUnitOfWork(CleaningUnitOfWorkInterface):

    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory()

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.cleaning = CleaningSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
