from unittest import mock

from banneret import remove_all, CONFIGS, CACHES, PLUGINS, LOGS


@mock.patch('banneret.remove')
class TestOSSupport:

    @mock.patch('sys.platform', 'win32')
    def test_windows_is_not_supported(self, mock_remove):
        remove_all()
        mock_remove.assert_not_called()

    @mock.patch('sys.platform', 'linux')
    def test_linux_is_not_supported(self, mock_remove):
        remove_all()
        mock_remove.assert_not_called()

    @mock.patch('sys.platform', 'darwin')
    def test_mac_is_supported(self, mock_remove):
        remove_all()
        assert mock_remove.call_count == 4


@mock.patch('sys.platform', 'darwin')
@mock.patch('banneret.remove')
class TestArgumentsLogic:

    def test_remove_all(self, mock_remove):
        remove_all()
        assert mock_remove.call_count == 4

    def test_remove_configs(self, mock_remove):
        remove_all(configs=True)
        mock_remove.assert_called_once_with(CONFIGS, 'PyCharm*')

    def test_remove_caches(self, mock_remove):
        remove_all(caches=True)
        mock_remove.assert_called_once_with(CACHES, 'PyCharm*')

    def test_remove_plugins(self, mock_remove):
        remove_all(plugins=True)
        mock_remove.assert_called_once_with(PLUGINS, 'PyCharm*')

    def test_remove_logs(self, mock_remove):
        remove_all(logs=True)
        mock_remove.assert_called_once_with(LOGS, 'PyCharm*')
