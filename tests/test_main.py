from unittest import mock

from banneret import main
from tests.conftest import mock_argv


@mock.patch('banneret.clean_settings')
@mock_argv('clean')
def test_pure_clean(mock_clean_settings):
    main()
    mock_clean_settings.assert_called_once()
    args = mock_clean_settings.call_args[0][0]
    assert args.command == 'clean'
    assert not args.version
    assert not args.configs
    assert not args.caches
    assert not args.plugins
    assert not args.logs


@mock.patch('banneret.clean_settings')
@mock_argv('clean', 'PyCharm2016.3', '-Ccpl')
def test_all_options_clean(mock_clean_settings):
    main()
    mock_clean_settings.assert_called_once()
    args = mock_clean_settings.call_args[0][0]
    assert args.command == 'clean'
    assert args.version == 'PyCharm2016.3'
    assert args.configs
    assert args.caches
    assert args.plugins
    assert args.logs
