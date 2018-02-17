import pytest

from banneret.main import main, run_clean_command, run_archive_command, \
    run_docker_command, run_enable_errors_command


@pytest.fixture(name='mock_run_clean_command')
def fixture_mock_rcc(mocker):
    mock_rcc = mocker.patch('banneret.main.run_clean_command')
    yield mock_rcc


@pytest.fixture(name='mock_run_archive_command')
def fixture_mock_rac(mocker):
    mock_rac = mocker.patch('banneret.main.run_archive_command')
    yield mock_rac


@pytest.fixture(name='mock_run_docker_command')
def fixture_mock_rdc(mocker):
    mock_rdc = mocker.patch('banneret.main.run_docker_command')
    yield mock_rdc


@pytest.fixture(name='mock_input')
def fixture_mock_import(mocker):
    mock_input = mocker.patch('banneret.main.input')
    yield mock_input


@pytest.fixture(name='mock_remove_all')
def fixture_mock_remove_all(mocker):
    mock_remove_all = mocker.patch('banneret.main.remove_all')
    yield mock_remove_all


@pytest.fixture(name='mock_archive_project')
def fixture_mock_archive_project(mocker):
    mock_archive_project = mocker.patch('banneret.main.archive_project')
    yield mock_archive_project


@pytest.fixture(name='mock_clean_docker')
def fixture_mock_clean_docker(mocker):
    mock_clean_docker = mocker.patch('banneret.main.clean_docker')
    yield mock_clean_docker


@pytest.fixture(name='mock_enable_errors')
def fixture_mock_enable_errors(mocker):
    mock_enable_errors = mocker.patch('banneret.main.enable_errors')
    yield mock_enable_errors


@pytest.mark.usefixtures('command')
@pytest.mark.parametrize('command', [''], indirect=True)
class TestOSSupport:

    @pytest.mark.usefixtures('win32')
    def test_windows_is_not_supported(self, log):
        with pytest.raises(SystemExit):
            main()
        assert 'Wrong os: win32' in log.text

    @pytest.mark.usefixtures('linux')
    def test_linux_is_not_supported(self, log):
        with pytest.raises(SystemExit):
            main()
        assert 'Wrong os: linux' in log.text

    @pytest.mark.usefixtures('darwin')
    def test_mac_is_supported(self, log):
        with pytest.raises(SystemExit):
            main()
        assert 'Wrong os' not in log.text


@pytest.mark.usefixtures('command', 'darwin')
class TestRunCommand:

    @pytest.mark.parametrize('command', ['clean'], indirect=True)
    def test_clean(self, mock_run_clean_command):
        main()
        mock_run_clean_command.assert_called_once()

    @pytest.mark.parametrize('command', ['archive'], indirect=True)
    def test_archive(self, mock_run_archive_command):
        main()
        mock_run_archive_command.assert_called_once()

    @pytest.mark.parametrize('command', ['docker'], indirect=True)
    def test_docker(self, mock_run_docker_command):
        main()
        mock_run_docker_command.assert_called_once()


class TestRunCleanCommand:

    def test_wrong_version(self, mock_remove_all, mock_input, args):
        args.version = 'abc'
        with pytest.raises(SystemExit):
            run_clean_command(args)
        mock_remove_all.assert_not_called()
        mock_input.assert_not_called()

    def test_correct_version(self, mock_remove_all, mock_input, args):
        args.version = 'pycharm2017.2'
        run_clean_command(args)
        mock_remove_all.assert_called_once()
        mock_input.assert_not_called()

    def test_remove_all(self, mock_remove_all, mock_input, args):
        args.version = 'pycharm'
        mock_input.return_value = 'yes'
        run_clean_command(args)
        mock_remove_all.assert_called_once()
        mock_input.assert_called_once()

    def test_remove_all_abort(self, mock_remove_all, mock_input, args):
        args.version = 'pycharm'
        mock_input.return_value = 'no'
        with pytest.raises(SystemExit):
            run_clean_command(args)
        mock_remove_all.assert_not_called()
        mock_input.assert_called_once()

    def test_nothing_to_remove(self, mock_remove_all, mock_input, args):
        args.version = 'pycharm2017.2'
        mock_remove_all.return_value = False
        with pytest.raises(SystemExit):
            run_clean_command(args)
        mock_remove_all.assert_called_once()
        mock_input.assert_not_called()


class TestRunArchiveCommand:

    def test_unknown_project_or_target(self, mock_archive_project, args):
        mock_archive_project.side_effect = IOError
        with pytest.raises(SystemExit):
            run_archive_command(args)
        mock_archive_project.assert_called_once()

    def test_correct_run(self, mock_archive_project, args):
        run_archive_command(args)
        mock_archive_project.assert_called_once()


class TestRunDockerCommand:

    def test_docker_is_not_installed(self, mock_clean_docker, args, mocker):
        mocker.patch('banneret.main.docker', None)
        with pytest.raises(SystemExit):
            run_docker_command(args)
        mock_clean_docker.assert_not_called()

    def test_remove_only_something(self, mock_clean_docker, args):
        args.containers = False
        args.images = True
        args.volumes = False

        run_docker_command(args)
        mock_clean_docker.assert_called_with(False, True, False)

    def test_remove_everything(self, mock_input, mock_clean_docker, args):
        args.containers = False
        args.images = False
        args.volumes = False
        mock_input.return_value = 'yes'

        run_docker_command(args)
        mock_clean_docker.assert_called_with()
        mock_input.assert_called_once()

    def test_remove_all_abort(self, mock_input, mock_clean_docker, args):
        args.containers = False
        args.images = False
        args.volumes = False
        mock_input.return_value = 'no'

        with pytest.raises(SystemExit):
            run_docker_command(args)
        mock_clean_docker.assert_not_called()
        mock_input.assert_called_once()


class TestRunErrorsCommand:

    def test_wrong_version(self, mock_enable_errors, mock_input, args):
        args.version = 'abc'
        with pytest.raises(SystemExit):
            run_enable_errors_command(args)
            mock_enable_errors.assert_not_called()
        mock_input.assert_not_called()

    def test_correct_version(self, mock_enable_errors, mock_input, args):
        args.version = 'pycharm2017.3'
        run_enable_errors_command(args)
        mock_enable_errors.assert_called_once()
        mock_input.assert_not_called()

    def test_switch_for_all(self, mock_enable_errors, mock_input, args):
        args.version = 'pycharm'
        mock_input.return_value = 'yes'
        run_enable_errors_command(args)
        mock_enable_errors.assert_called_once()
        mock_input.assert_called_once()

    def test_switch_for_all_abort(self, mock_enable_errors, mock_input,
                                  args):
        args.version = 'pycharm'
        mock_input.return_value = 'no'
        with pytest.raises(SystemExit):
            run_enable_errors_command(args)
        mock_enable_errors.assert_not_called()
        mock_input.assert_called_once()

    def test_no_settings_was_found(self, mock_enable_errors, mock_input, args):
        mock_enable_errors.side_effect = IOError
        args.version = 'pycharm'
        mock_input.return_value = 'yes'
        with pytest.raises(SystemExit):
            run_enable_errors_command(args)
        mock_enable_errors.assert_called_once()
        mock_input.assert_called_once()
