from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chatcleaner.adapters.services.chat import ChatService
from chatcleaner.adapters.unit_of_works.cleaning import CleaningSqlAlchemyUnitOfWork
from chatcleaner.adapters.use_cases.clean import CleanUseCase
from chatcleaner.configurator.settings import get_database_uri

# Hard code the db connection for now
db_uri = get_database_uri()
ENGINE = create_engine(db_uri)


class FakeContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "chatcleaner.adapters.use_cases.clean",
        ],
    )
    DEFAULT_SESSION_FACTORY = lambda: sessionmaker(bind=ENGINE, autocommit=False)

    cleaning_uow = providers.Factory(
        CleaningSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    chat_service = providers.Factory(ChatService)

    cleaning_use_case = providers.Factory(
        CleanUseCase,
        uow=cleaning_uow,
        service=chat_service,
    )
