import logging
import sys

import pytest
from click.testing import CliRunner

only_macos = pytest.mark.skipif(sys.platform != 'darwin', reason='Not macOS')


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def client(mocker):
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
def mock_remove_all(mocker):
    yield mocker.patch('banneret.main.remove_all')


@pytest.fixture
def mock_archive_project(mocker):
    yield mocker.patch('banneret.main.archive_project')


@pytest.fixture
def mock_clean_docker(mocker):
    yield mocker.patch('banneret.main.clean_docker')


@pytest.fixture
def mock_enable_errors(mocker):
    yield mocker.patch('banneret.main.enable_errors')
