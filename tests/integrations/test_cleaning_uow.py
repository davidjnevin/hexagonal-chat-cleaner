import pytest


@pytest.mark.integration
def test_uow_add_cleaning(get_fake_container, get_cleaning_model_object):
    uow = get_fake_container.cleaning_uow()
    with uow:
        uow.cleaning.add(get_cleaning_model_object)
        uow.commit()
        all_ = uow.cleaning.get_all()
        assert len(all_) == 1
        assert all_[0].cleaned_chat == "test"
