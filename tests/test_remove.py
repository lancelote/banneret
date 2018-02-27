def test_removes_correct_dir(base_path, bnrt):
    remove_me = 'PyCharm2017.2'
    for folder in ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']:
        base_path.mkdir(folder)
    bnrt.remove(base_path, 'PyCharm2017.2')
    assert len(base_path.listdir()) == 2
    assert remove_me not in base_path.listdir()


def test_nothing_to_remove(base_path, bnrt):
    assert not bnrt.remove(base_path, 'PyCharm*')


def test_removes_everything(base_path, bnrt):
    do_not_remove = base_path.mkdir('do_no_remove')
    for folder in ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']:
        base_path.mkdir(folder)
    bnrt.remove(base_path, 'PyCharm*')
    assert base_path.listdir() == [do_not_remove]


def test_unknown_path(bnrt):
    assert not bnrt.remove('qwerty', 'PyCharm*')


class TestReturnCorrectStatus:

    def test_remove_returns_false_if_nothing_was_removed(self, bnrt):
        result = bnrt.remove('unknown_path', 'version')
        assert not result

    def test_returns_true_if_something_was_removed(self, base_path, bnrt):
        base_path.mkdir('PyCharm2017.2')
        result = bnrt.remove(base_path, 'PyCharm2017.2')
        assert result
