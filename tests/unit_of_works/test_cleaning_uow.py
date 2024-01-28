def test_uow_add_cleaning(get_fake_uow, get_cleaning_model_object):
    with get_fake_uow as uow:
        uow.cleaning.add(get_cleaning_model_object)
        all_ = uow.cleaning.get_all()
        values = all_
        assert len(values) == 1
        assert values[0].cleaned_chat == "test"


def test_uow_get_cleaning_by_uuid(get_fake_uow, get_cleaning_model_object):
    with get_fake_uow as uow:
        uow.cleaning.add(get_cleaning_model_object)
        all_ = uow.cleaning.get_all()
        values = all_
        uuid = values[0].uuid
        result = uow.cleaning.get_by_uuid(uuid)
        assert result.cleaned_chat == "test"


def test_uow_get_all_cleanings(get_fake_uow, get_cleaning_model_object):
    with get_fake_uow as uow:
        uow.cleaning.add(get_cleaning_model_object)
        uow.cleaning.add(get_cleaning_model_object)
        all_ = uow.cleaning.get_all()
        values = all_
        assert len(values) == 2
        assert values[0].cleaned_chat == "test"
        assert values[1].cleaned_chat == "test"
