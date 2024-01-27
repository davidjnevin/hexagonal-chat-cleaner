# fixtures are scoped to module


def test_add_cleaning(get_fake_repository, get_cleaning_model_object):
    get_fake_repository.add(get_cleaning_model_object)
    all_ = get_fake_repository.get_all()

    values = all_
    assert len(values) == 1
    assert values[0].cleaned_chat == "test"


def test_cleaning_by_uuid(get_fake_repository):
    all_ = get_fake_repository.get_all()
    values = all_
    uuid = values[0].uuid
    result = get_fake_repository.get_by_uuid(uuid)
    assert result.cleaned_chat == "test"


def test_get_all_cleanings(get_fake_repository, get_cleaning_model_object):
    all_ = get_fake_repository.get_all()
    values = all_
    assert len(values) == 1

    get_fake_repository.add(get_cleaning_model_object)

    all_ = get_fake_repository.get_all()
    values = all_
    assert len(values) == 2
    assert values[0].cleaned_chat == "test"
    assert values[1].cleaned_chat == "test"
