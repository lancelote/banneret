import pytest

from banneret.main import remove_all, CONFIGS, CACHES, PLUGINS, LOGS


@pytest.fixture(name='mock_remove')
def fixture_mock_remove(mocker):
    mock_remove = mocker.patch('banneret.main.remove')
    yield mock_remove


@pytest.fixture(name='_mock_win32')
def fixture_mock_win32(mocker):
    mocker.patch('sys.platform', 'win32')
    yield


@pytest.fixture(name='_mock_linux')
def fixture_mock_linux(mocker):
    mocker.patch('sys.platform', 'linux')
    yield


@pytest.fixture(name='_mock_darwin')
def fixture_mock_darwin(mocker):
    mocker.patch('sys.platform', 'darwin')
    yield


class TestOSSupport:

    def test_windows_is_not_supported(self, mock_remove, _mock_win32):
        remove_all('PyCharm*')
        mock_remove.assert_not_called()

    def test_linux_is_not_supported(self, mock_remove, _mock_linux):
        remove_all('PyCharm*')
        mock_remove.assert_not_called()

    def test_mac_is_supported(self, mock_remove, _mock_darwin):
        remove_all('PyCharm*')
        assert mock_remove.call_count == 4


@pytest.mark.usefixtures('_mock_darwin')
class TestArgumentsLogic:

    def test_remove_all(self, mock_remove):
        remove_all('PyCharm*')
        assert mock_remove.call_count == 4

    def test_remove_configs(self, mock_remove):
        remove_all('PyCharm*', configs=True)
        mock_remove.assert_called_once_with(CONFIGS, 'PyCharm*')

    def test_remove_caches(self, mock_remove):
        remove_all('PyCharm*', caches=True)
        mock_remove.assert_called_once_with(CACHES, 'PyCharm*')

    def test_remove_plugins(self, mock_remove):
        remove_all('PyCharm*', plugins=True)
        mock_remove.assert_called_once_with(PLUGINS, 'PyCharm*')

    def test_remove_logs(self, mock_remove):
        remove_all('PyCharm*', logs=True)
        mock_remove.assert_called_once_with(LOGS, 'PyCharm*')


@pytest.mark.usefixtures('_mock_darwin')
class TestReturnStatus:

    def test_nothing_was_removed(self, mock_remove):
        mock_remove.return_value = False
        result = remove_all('PyCharm*')
        assert not result

    def test_everything_was_removed(self, mock_remove):
        mock_remove.return_value = True
        result = remove_all('PyCharm*')
        assert result

    def test_only_logs_were_removed(self, mock_remove):
        mock_remove.side_effect = [False, False, False, True]
        result = remove_all('PyCharm*')
        assert result

    def test_only_plugins_were_removed(self, mock_remove):
        mock_remove.side_effect = [False, False, True, False]
        result = remove_all('PyCharm*')
        assert result

    def test_only_plugins_and_logs_were_removed(self, mock_remove):
        mock_remove.side_effect = [False, False, True, True]
        result = remove_all('PyCharm*')
        assert result
