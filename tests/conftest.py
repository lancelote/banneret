import logging

import pytest
from click.testing import CliRunner

from banneret.main import BanneretMacOS, Docker


@pytest.fixture
def bnrt():
    return BanneretMacOS()


@pytest.fixture
def docker_daemon():
    return Docker()


@pytest.fixture
def runner():
    return CliRunner()


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
def mock_remove(mocker):
    yield mocker.patch('banneret.main.BanneretMacOS.remove')


@pytest.fixture
def mock_remove_all(mocker):
    yield mocker.patch('banneret.main.BanneretMacOS.remove_all')


@pytest.fixture
def mock_archive_project(mocker):
    yield mocker.patch('banneret.main.BanneretMacOS.archive_project')


@pytest.fixture
def mock_clean_docker(mocker):
    yield mocker.patch('banneret.main.BanneretMacOS.clean_docker')


@pytest.fixture
def mock_enable_error(mocker):
    yield mocker.patch('banneret.main.BanneretMacOS.enable_error')


@pytest.fixture
def mock_enable_errors(mocker):
    yield mocker.patch('banneret.main.BanneretMacOS.enable_errors')


@pytest.fixture
def mock_remove_containers(mocker):
    yield mocker.patch('banneret.main.Docker.remove_containers')


@pytest.fixture
def mock_remove_images(mocker):
    yield mocker.patch('banneret.main.Docker.remove_images')


@pytest.fixture
def mock_remove_volumes(mocker):
    yield mocker.patch('banneret.main.Docker.remove_volumes')
