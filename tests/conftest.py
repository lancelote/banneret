from unittest import mock

import pytest

from banneret import create_parser


@pytest.fixture
def parser():
    return create_parser()


@pytest.fixture
def client():
    return mock.Mock()


@pytest.fixture
def args():
    return mock.Mock()
