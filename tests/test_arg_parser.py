import pytest


def test_no_args(parser):
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_unknown_command(parser):
    with pytest.raises(SystemExit):
        parser.parse_args(['ls'])


def test_clean_without_args(parser):
    args = parser.parse_args(['clean'])
    assert args.command == 'clean'
    assert not args.version
    assert not args.configs
    assert not args.caches
    assert not args.plugins
    assert not args.logs


def test_clean_with_version(parser):
    args = parser.parse_args(['clean', 'PyCharm2017.2'])
    assert args.command == 'clean'
    assert args.version == 'PyCharm2017.2'


def test_clean_with_version_and_all_flags(parser):
    args = parser.parse_args(['clean', '-Ccpl', 'PyCharm2017.1'])
    assert args.command == 'clean'
    assert args.version == 'PyCharm2017.1'
    assert args.configs
    assert args.caches
    assert args.plugins
    assert args.logs


@pytest.mark.parametrize('flag', ['-C', '--configs'])
def test_clean_configs(parser, flag):
    args = parser.parse_args(['clean', flag])
    assert args.configs
    assert not args.caches
    assert not args.plugins
    assert not args.logs


@pytest.mark.parametrize('flag', ['-c', '--caches'])
def test_clean_caches(parser, flag):
    args = parser.parse_args(['clean', flag])
    assert args.caches
    assert not args.configs
    assert not args.plugins
    assert not args.logs


@pytest.mark.parametrize('flag', ['-p', '--plugins'])
def test_clean_plugins(parser, flag):
    args = parser.parse_args(['clean', flag])
    assert args.plugins
    assert not args.configs
    assert not args.caches
    assert not args.logs


@pytest.mark.parametrize('flag', ['-l', '--logs'])
def test_clean_logs(parser, flag):
    args = parser.parse_args(['clean', flag])
    assert args.logs
    assert not args.configs
    assert not args.caches
    assert not args.plugins
