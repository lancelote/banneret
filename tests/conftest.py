import pytest

from banneret.main import create_parser


@pytest.fixture
def parser():
    return create_parser()


@pytest.fixture
def client(mocker):
    return mocker.Mock()


@pytest.fixture
def args(mocker):
    return mocker.Mock()


@pytest.fixture
def base_path(tmpdir):
    return tmpdir.mkdir('base_path')
