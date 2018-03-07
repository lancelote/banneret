from banneret.main import CONFIGS, CACHES, PLUGINS, LOGS, HOME
from tests.conftest import only_linux, only_mac


class TestArgumentsLogic:

    @only_mac
    def test_remove_all(self, mock_remove, bnrt):
        bnrt.remove_all('PyCharm*')
        assert mock_remove.call_count == 4

    @only_linux
    def test_remove_all(self, mock_remove, bnrt):
        bnrt.remove_all('PyCharm*')
        mock_remove.assert_called_once_with(HOME + '/{version}', 'PyCharm*')

    def test_remove_configs(self, mock_remove, bnrt):
        bnrt.remove_all('PyCharm*', configs=True)
        mock_remove.assert_called_once_with(CONFIGS, 'PyCharm*')

    def test_remove_caches(self, mock_remove, bnrt):
        bnrt.remove_all('PyCharm*', caches=True)
        mock_remove.assert_called_once_with(CACHES, 'PyCharm*')

    def test_remove_plugins(self, mock_remove, bnrt):
        bnrt.remove_all('PyCharm*', plugins=True)
        mock_remove.assert_called_once_with(PLUGINS, 'PyCharm*')

    def test_remove_logs(self, mock_remove, bnrt):
        bnrt.remove_all('PyCharm*', logs=True)
        mock_remove.assert_called_once_with(LOGS, 'PyCharm*')


class TestReturnStatus:

    def test_nothing_was_removed(self, mock_remove, bnrt):
        mock_remove.return_value = False
        result = bnrt.remove_all('PyCharm*')
        assert not result

    def test_everything_was_removed(self, mock_remove, bnrt):
        mock_remove.return_value = True
        result = bnrt.remove_all('PyCharm*')
        assert result

    def test_only_logs_were_removed(self, mock_remove, bnrt):
        result = bnrt.remove_all('PyCharm*', logs=True)
        mock_remove.assert_called_once_with(LOGS, 'PyCharm*')
        assert result

    def test_only_plugins_were_removed(self, mock_remove, bnrt):
        result = bnrt.remove_all('PyCharm*', plugins=True)
        mock_remove.assert_called_once_with(PLUGINS, 'PyCharm*')
        assert result

    def test_only_plugins_and_logs_were_removed(self, mock_remove, bnrt):
        result = bnrt.remove_all('PyCharm*', plugins=True, logs=True)
        assert mock_remove.call_count == 2
        assert result
