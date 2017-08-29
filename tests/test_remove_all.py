from unittest import mock

from banneret import remove_all


@mock.patch('banneret.remove')
class TestRemoveAll:

    @mock.patch('sys.platform', 'win32')
    def test_windows_is_not_supported(self, mock_remove):
        remove_all(*[True]*5)
        mock_remove.assert_not_called()

    @mock.patch('sys.platform', 'linux')
    def test_linux_is_not_supported(self, mock_remove):
        remove_all(*[True]*5)
        mock_remove.assert_not_called()

    @mock.patch('sys.platform', 'darwin')
    def test_mac_is_supported(self, mock_remove):
        remove_all(*[True]*5)
        assert mock_remove.call_count == 4
