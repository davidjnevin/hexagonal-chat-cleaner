import pytest

from chatcleaner.configurator.containers import Container


@pytest.mark.integration
def test_clean_use_case_clean(get_fake_container, get_clean_use_case):
    with Container.cleaning_uow.override(get_fake_container.cleaning_uow):
        with Container.chat_service.override(get_fake_container.chat_service):
            get_clean_use_case.clean("\n19:10:00 from David to Everyone:\ntest")
            uow_ = get_fake_container.cleaning_uow()
            with uow_:
                result = uow_.cleaning.get_all()
                assert len(result) == 1
                assert result[0].chat == "\n19:10:00 from David to Everyone:\ntest"
                assert result[0].cleaned_chat == "test"


@pytest.mark.integration
def test_clean_use_case_get_all(get_fake_container, get_clean_use_case):
    with Container.cleaning_uow.override(get_fake_container.cleaning_uow):
        with Container.chat_service.override(get_fake_container.chat_service):
            get_clean_use_case.clean("\n19:10:00 from David to Everyone:\ntest 1")
            get_clean_use_case.clean("\n19:10:00 from David to Everyone:\ntest 2")
            get_clean_use_case.clean("\n19:10:00 from David to Everyone:\ntest 3")
            uow_ = get_fake_container.cleaning_uow()
            with uow_:
                result = get_clean_use_case.get_all()
                # fixtures are scopes to module, so this should be 4
                assert len(result["results"]) == 4
                # breakpoint()
                # assert result[0].chat == "\n19:10:00 from David to Everyone:\ntest"
                # assert result[0].cleaned_chat == "test"
                # assert result[1].chat == "\n19:10:00 from David to Everyone:\ntest 1"
                # assert result[1].cleaned_chat == "test 1"
                # assert result[2].chat == "\n19:10:00 from David to Everyone:\ntest 2"
                # assert result[2].cleaned_chat == "test 2"
                # assert result[3].chat == "\n19:10:00 from David to Everyone:\ntest 3"
                # assert result[3].cleaned_chat == "test 3"


@pytest.mark.integration
def test_clean_use_case_get_by_id(get_fake_container, get_clean_use_case):
    with Container.cleaning_uow.override(get_fake_container.cleaning_uow):
        with Container.chat_service.override(get_fake_container.chat_service):
            result = get_clean_use_case.get_all()
            uuid_ = result["results"][0]
            assert uuid_
            data = get_clean_use_case.get_by_uuid(uuid_)
            assert data["result"]["uuid"] == uuid_
            data = get_clean_use_case.get_by_uuid("fake")
            assert data["result"] == "Not found"
