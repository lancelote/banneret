import sys

from banneret.cli import MACOS, LINUX
from tests.conftest import create_settings


def call_remove(path, version, bnrt):
    """Call remove method depending on the OS."""
    if sys.platform in MACOS:
        result = bnrt.remove(path, version)
    elif sys.platform in LINUX:
        result = bnrt.remove(path + '/.{version}', version)
    else:
        raise OSError('Unsupported OS')
    return result


def test_removes_correct_dir(base_path, bnrt):
    remove_me = 'PyCharm2017.2'
    versions = ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']
    create_settings(base_path, versions)
    call_remove(base_path, remove_me, bnrt)
    assert len(base_path.listdir()) == 2
    assert remove_me not in base_path.listdir()


def test_nothing_to_remove(base_path, bnrt):
    assert not call_remove(base_path, 'PyCharm*', bnrt)


def test_removes_everything(base_path, bnrt):
    do_not_remove = base_path.mkdir('do_no_remove')
    versions = ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']
    create_settings(base_path, versions)
    call_remove(base_path, 'PyCharm*', bnrt)
    assert base_path.listdir() == [do_not_remove]


def test_unknown_path(bnrt):
    assert not call_remove('qwerty', 'PyCharm*', bnrt)


def test_remove_returns_false_if_nothing_was_removed(bnrt):
    assert not call_remove('unknown_path', 'version', bnrt)


def test_returns_true_if_something_was_removed(base_path, bnrt):
    create_settings(base_path, ['PyCharm2017.2'])
    assert call_remove(base_path, 'PyCharm2017.2', bnrt)
