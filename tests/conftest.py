import logging

import pytest

from banneret.main import create_parser


@pytest.fixture
def parser():
    return create_parser()


@pytest.fixture
def mock_parser(mocker):
    mock_parser = mocker.patch('banneret.main.create_parser')
    yield mock_parser


@pytest.fixture
def client(mocker):
    return mocker.Mock()


@pytest.fixture
def args(mocker):
    return mocker.Mock()


@pytest.fixture
def base_path(tmpdir):
    return tmpdir.mkdir('base_path')


@pytest.fixture
def log(caplog):
    caplog.set_level(logging.INFO)
    return caplog


@pytest.fixture
def win32(mocker):
    mocker.patch('sys.platform', 'win32')
    yield


@pytest.fixture
def linux(mocker):
    mocker.patch('sys.platform', 'linux')
    yield


@pytest.fixture
def darwin(mocker):
    mocker.patch('sys.platform', 'darwin')
    yield


@pytest.fixture
def command(request, mock_parser):
    mock_parser().parse_args().command = request.param
    yield
