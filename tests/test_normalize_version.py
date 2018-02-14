import pytest

from banneret.main import normalize_version


def test_ide_is_not_supported():
    with pytest.raises(ValueError):
        normalize_version('Ruby2017.2')


def test_incorrect_target():
    with pytest.raises(ValueError):
        normalize_version('2017.2')


def test_no_version():
    ide, version = normalize_version('pycharm')
    assert ide == 'PyCharm'
    assert version == '*'


def test_ide_and_version():
    ide, version = normalize_version('idea2017.2')
    assert ide == 'IntelliJIdea'
    assert version == '2017.2'


def test_pycharm_community_edition_is_supported():
    ide, version = normalize_version('pycharmce2017.2')
    assert ide == 'PyCharmCE'
    assert version == '2017.2'


def test_idea_community_is_supported():
    ide, version = normalize_version('ideaic2017.3')
    assert ide == 'IdeaIC'
    assert version == '2017.3'
