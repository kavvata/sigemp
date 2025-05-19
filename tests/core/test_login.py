from unittest import mock

import pytest

from core.types import ResultError, ResultSuccess
from core.usecases import login_usecase


@pytest.fixture
def user_credentials():
    return {"username": "usuario", "password": "supersenha"}


def test_login_usecase_success(user_credentials):
    repo = mock.Mock()
    repo.authenticate.return_value = user_credentials

    result = login_usecase(
        user_credentials["username"], user_credentials["password"], repo
    )

    repo.authenticate.assert_called_with(
        user_credentials["username"], user_credentials["password"]
    )
    assert result
    assert isinstance(result, ResultSuccess)
    assert result.value == user_credentials


def test_login_usecase_failed(user_credentials):
    repo = mock.Mock()
    repo.authenticate.return_value = None

    result = login_usecase(
        user_credentials["username"], user_credentials["password"], repo
    )

    repo.authenticate.assert_called_with(
        user_credentials["username"], user_credentials["password"]
    )
    assert not result
    assert isinstance(result, ResultError)
    assert result.mensagem
