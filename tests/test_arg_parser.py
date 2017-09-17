import pytest

from banneret import PWD, HOME


class TestGeneral:

    def test_no_args(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_unknown_command(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args(['ls'])


class TestClean:

    def test_version_is_required(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args(['clean'])

    def test_clean_without_flags(self, parser):
        args = parser.parse_args(['clean', 'pycharm'])
        assert args.command == 'clean'
        assert args.version == 'pycharm'
        assert not args.configs
        assert not args.caches
        assert not args.plugins
        assert not args.logs

    def test_clean_with_version_and_all_flags(self, parser):
        args = parser.parse_args(['clean', '-Ccpl', 'PyCharm2017.1'])
        assert args.command == 'clean'
        assert args.version == 'PyCharm2017.1'
        assert args.configs
        assert args.caches
        assert args.plugins
        assert args.logs

    @pytest.mark.parametrize('flag', ['-C', '--configs'])
    def test_clean_configs(self, parser, flag):
        args = parser.parse_args(['clean', 'pycharm', flag])
        assert args.configs
        assert not args.caches
        assert not args.plugins
        assert not args.logs

    @pytest.mark.parametrize('flag', ['-c', '--caches'])
    def test_clean_caches(self, parser, flag):
        args = parser.parse_args(['clean', 'pycharm', flag])
        assert args.caches
        assert not args.configs
        assert not args.plugins
        assert not args.logs

    @pytest.mark.parametrize('flag', ['-p', '--plugins'])
    def test_clean_plugins(self, parser, flag):
        args = parser.parse_args(['clean', 'pycharm', flag])
        assert args.plugins
        assert not args.configs
        assert not args.caches
        assert not args.logs

    @pytest.mark.parametrize('flag', ['-l', '--logs'])
    def test_clean_logs(self, parser, flag):
        args = parser.parse_args(['clean', 'pycharm', flag])
        assert args.logs
        assert not args.configs
        assert not args.caches
        assert not args.plugins


class TestZip:

    def test_archive_without_args(self, parser):
        args = parser.parse_args(['archive'])
        assert args.command == 'archive'
        assert args.target == f'{HOME}/Desktop'
        assert args.project == PWD

    @pytest.mark.parametrize('flag', ['-t', '--target'])
    def test_archive_with_target(self, parser, flag):
        args = parser.parse_args(['archive', flag, 'target'])
        assert args.command == 'archive'
        assert args.target == 'target'
        assert args.project == PWD

    @pytest.mark.parametrize('flag', ['-p', '--project'])
    def test_archive_with_project(self, parser, flag):
        args = parser.parse_args(['archive', flag, 'project'])
        assert args.command == 'archive'
        assert args.target == f'{HOME}/Desktop'
        assert args.project == 'project'

    def test_archive_with_target_and_project(self, parser):
        args = parser.parse_args(['archive', '-t', 'target', '-p', 'project'])
        assert args.command == 'archive'
        assert args.target == 'target'
        assert args.project == 'project'


class TestDocker:

    def test_without_flags(self, parser):
        args = parser.parse_args(['docker'])
        assert not args.containers
        assert not args.images
        assert not args.volumes

    def test_remove_only_containers(self, parser):
        args = parser.parse_args('docker -c'.split())
        assert args.containers
        assert not args.images
        assert not args.volumes

    def test_remove_only_images(self, parser):
        args = parser.parse_args('docker -i'.split())
        assert not args.containers
        assert args.images
        assert not args.volumes

    def test_remove_only_volumes(self, parser):
        args = parser.parse_args('docker -v'.split())
        assert not args.containers
        assert not args.images
        assert args.volumes

    def test_remove_containers_and_volumes(self, parser):
        args = parser.parse_args('docker -cv'.split())
        assert args.containers
        assert not args.images
        assert args.volumes


class TestErrors:

    def test_no_version(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args(['errors'])

    def test_without_flags(self, parser):
        args = parser.parse_args(['errors', 'pycharm'])
        assert args.version == 'pycharm'
        assert not args.disable

    @pytest.mark.parametrize('flag', ['-d', '--disable'])
    def test_disable(self, parser, flag):
        args = parser.parse_args(['errors', 'pycharm', flag])
        assert args.version == 'pycharm'
        assert args.disable
