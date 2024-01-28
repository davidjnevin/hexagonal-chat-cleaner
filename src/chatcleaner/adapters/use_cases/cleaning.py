from chatcleaner.domain.ports.services.cleaning import CleaningServiceInterface
from chatcleaner.domain.ports.unit_of_works.cleaning import CleaningUnitOfWorkInterface
from chatcleaner.domain.ports.use_cases.cleaning import CleaningUseCaseInterface


class CleaningUseCase(CleaningUseCaseInterface):
    def __init__(
        self, uow: CleaningUnitOfWorkInterface, service: CleaningServiceInterface
    ):
        self.uow = uow
        self.service = service

    def add(self, cleaning):
        with self.uow:
            self.uow.cleaning.add(cleaning)
            self.uow.commit()
