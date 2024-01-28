from chatcleaner.domain.ports.unit_of_works.cleaning import CleaningUnitOfWorkInterface
from tests.fake_repository import FakeCleaningRepository


class FakeCleaningUnitOfWork(CleaningUnitOfWorkInterface):
    def __init__(self):
        self.commited = False

    def __enter__(self):
        self.cleaning = FakeCleaningRepository()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        self.commited = True

    def rollback(self):
        # because it is unimportant
        pass
