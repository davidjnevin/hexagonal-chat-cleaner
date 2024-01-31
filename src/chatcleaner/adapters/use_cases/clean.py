from typing import Any

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

    def _clean(self, chat_text: str):
        with self.uow:
            # clean
            result = self.service.clean(chat_text)
            # save
            schema_ = CleaningCreateDTO()
            data_ = schema_.load({"chat_text": chat_text, "cleaned_chat": result})
            model = cleaning_factory(**data_)
            self.uow.cleaning.add(model)
            self.uow.commit()
            return {
                "uuid": model.uuid,
                "chat_text": chat_text,
                "cleaned_chat": model.cleaned_chat,
            }

    def _get_all(self) -> dict[str, list]:
        data_ = {"results": []}
        with self.uow:
            results = self.uow.cleaning.get_all()
            for result in results:
                data_["results"].append(result.uuid)
            return data_

    def _get_by_uuid(self, uuid_: str) -> dict[str, Any]:
        with self.uow:
            result = self.uow.cleaning.get_by_uuid(uuid_)
            if result:
                return {"result": result.to_dict()}
            return {"result": "Not found"}
