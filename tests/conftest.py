import logging

import pytest
from click.testing import CliRunner

from banneret import Banneret, Docker


@pytest.fixture
def bnrt():
    return Banneret()


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
def mock_remove(mocker):
    yield mocker.patch('banneret.Banneret.remove')


@pytest.fixture
def mock_remove_all(mocker):
    yield mocker.patch('banneret.Banneret.remove_all')


@pytest.fixture
def mock_archive_project(mocker):
    yield mocker.patch('banneret.Banneret.archive_project')


@pytest.fixture
def mock_clean_docker(mocker):
    yield mocker.patch('banneret.Banneret.clean_docker')


@pytest.fixture
def mock_enable_error(mocker):
    yield mocker.patch('banneret.Banneret.enable_error')


@pytest.fixture
def mock_enable_errors(mocker):
    yield mocker.patch('banneret.Banneret.enable_errors')


@pytest.fixture
def mock_remove_containers(mocker):
    yield mocker.patch('banneret.Docker.remove_containers')


@pytest.fixture
def mock_remove_images(mocker):
    yield mocker.patch('banneret.Docker.remove_images')


@pytest.fixture
def mock_remove_volumes(mocker):
    yield mocker.patch('banneret.Docker.remove_volumes')
