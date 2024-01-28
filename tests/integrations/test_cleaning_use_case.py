from chatcleaner.configurator.containers import Container


def test_clean_use_case_add(get_fake_container, get_clean_use_case):
    with Container.cleaning_uow.override(get_fake_container.cleaning_uow):
        with Container.chat_service.override(get_fake_container.chat_service):
            get_clean_use_case.add("\n19:10:00 from David to Everyone:\ntest")
            uow_ = get_fake_container.cleaning_uow()
            with uow_:
                result = uow_.cleaning.get_all()
                assert len(result) == 1
                assert result[0].chat == "\n19:10:00 from David to Everyone:\ntest"
                assert result[0].cleaned_chat == "test"
