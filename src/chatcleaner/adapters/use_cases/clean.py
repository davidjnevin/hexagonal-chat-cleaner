from dependency_injector.wiring import Provide

from chatcleaner.domain.model.model import cleaning_factory
from chatcleaner.domain.model.schemas import CleaningCreateDTO
from chatcleaner.domain.ports.services.chat import ChatServiceInterface
from chatcleaner.domain.ports.unit_of_works.cleaning import CleaningUnitOfWorkInterface
from chatcleaner.domain.ports.use_cases.clean import CleanUseCaseInterface


class CleanUseCase(CleanUseCaseInterface):
    def __init__(
        self,
        uow: CleaningUnitOfWorkInterface = Provide["cleaning_uow"],
        service: ChatServiceInterface = Provide["chat_service"],
    ):
        self.uow = uow
        self.service = service

    def _clean(self, chat: str):
        with self.uow:
            # clean
            result = self.service.clean(chat)
            # save
            schema_ = CleaningCreateDTO()
            data_ = schema_.load({"chat": chat, "cleaned_chat": result})
            model = cleaning_factory(**data_)
            self.uow.cleaning.add(model)
            self.uow.commit()

    def _get_all(self):
        with self.uow:
            return self.uow.cleaning.get_all()
