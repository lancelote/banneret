from banneret import remove


def test_removes_correct_dir(tmpdir):
    base_path = tmpdir.mkdir('base_path')
    remove_me = 'PyCharm2017.2'
    for folder in ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']:
        base_path.mkdir(folder)
    remove(base_path, 'PyCharm2017.2')
    assert len(base_path.listdir()) == 2
    assert remove_me not in base_path.listdir()


def test_nothing_to_remove(tmpdir):
    base_path = tmpdir.mkdir('base_path')
    remove(base_path, 'PyCharm*')
    # no exception is raised


def test_removes_everything(tmpdir):
    base_path = tmpdir.mkdir('base_path')
    do_not_remove = base_path.mkdir('do_no_remove')
    for folder in ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']:
        base_path.mkdir(folder)
    remove(base_path, 'PyCharm*')
    assert base_path.listdir() == [do_not_remove]


def test_unknown_path():
    remove('qwerty', 'PyCharm*')
    # no exception is raised


class TestReturnCorrectStatus:

    def test_remove_returns_false_if_nothing_was_removed(self):
        result = remove('unknown_path', 'version')
        assert not result

    def test_remove_returns_true_if_something_was_removed(self, tmpdir):
        base_path = tmpdir.mkdir('base_path')
        base_path.mkdir('PyCharm2017.2')
        result = remove(base_path, 'PyCharm2017.2')
        assert result
