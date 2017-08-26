import pytest

from banneret import create_parser


@pytest.fixture
def parser():
    return create_parser()
