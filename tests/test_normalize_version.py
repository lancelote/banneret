import pytest


def test_ide_is_not_supported(bnrt):
    with pytest.raises(ValueError):
        bnrt.normalize_version('Ruby2017.2')


def test_incorrect_target(bnrt):
    with pytest.raises(ValueError):
        bnrt.normalize_version('2017.2')


def test_no_version(bnrt):
    ide, version = bnrt.normalize_version('pycharm')
    assert ide == 'PyCharm'
    assert version == '*'


def test_ide_and_version(bnrt):
    ide, version = bnrt.normalize_version('idea2017.2')
    assert ide == 'IntelliJIdea'
    assert version == '2017.2'


def test_pycharm_community_edition_is_supported(bnrt):
    ide, version = bnrt.normalize_version('pycharmce2017.2')
    assert ide == 'PyCharmCE'
    assert version == '2017.2'


def test_idea_community_is_supported(bnrt):
    ide, version = bnrt.normalize_version('ideaic2017.3')
    assert ide == 'IdeaIC'
    assert version == '2017.3'
