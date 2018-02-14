try:
    from unittest import mock
except IndexError:
    import mock

import pytest

from banneret.main import main, run_clean_command, run_archive_command, \
    run_docker_command, run_enable_errors_command


@mock.patch('banneret.main.run_docker_command')
@mock.patch('banneret.main.run_archive_command')
@mock.patch('banneret.main.run_clean_command')
@mock.patch('banneret.main.create_parser')
class TestRunCommand:

    def test_clean(self, mock_parser, mock_rcc, mock_rac, mock_rdc):
        mock_parser().parse_args().command = 'clean'
        main()
        mock_rcc.assert_called_once()
        mock_rac.assert_not_called()
        mock_rdc.assert_not_called()

    def test_archive(self, mock_parser, mock_rcc, mock_rac, mock_rdc):
        mock_parser().parse_args().command = 'archive'
        main()
        mock_rcc.assert_not_called()
        mock_rac.assert_called_once()
        mock_rdc.assert_not_called()

    def test_docker(self, mock_parser, mock_rcc, mock_rac, mock_rdc):
        mock_parser().parse_args().command = 'docker'
        main()
        mock_rcc.assert_not_called()
        mock_rac.assert_not_called()
        mock_rdc.assert_called_once()


@mock.patch('banneret.main.input')
@mock.patch('banneret.main.remove_all')
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


@mock.patch('banneret.main.archive_project')
class TestRunArchiveCommand:

    def test_unknown_project_or_target(self, mock_archive_project, args):
        mock_archive_project.side_effect = FileNotFoundError
        with pytest.raises(SystemExit):
            run_archive_command(args)
        mock_archive_project.assert_called_once()

    def test_correct_run(self, mock_archive_project, args):
        run_archive_command(args)
        mock_archive_project.assert_called_once()


@mock.patch('banneret.main.clean_docker')
class TestRunDockerCommand:

    @mock.patch('banneret.main.docker', None)
    def test_docker_is_not_installed(self, mock_clean_docker, args):
        with pytest.raises(SystemExit):
            run_docker_command(args)
        mock_clean_docker.assert_not_called()

    def test_remove_only_something(self, mock_clean_docker, args):
        args.containers, args.images, args.volumes = False, True, False
        run_docker_command(args)
        mock_clean_docker.assert_called_with(False, True, False)

    @mock.patch('banneret.main.input')
    def test_remove_everything(self, mock_input, mock_clean_docker, args):
        args.containers, args.images, args.volumes = False, False, False
        mock_input.return_value = 'yes'
        run_docker_command(args)
        mock_clean_docker.assert_called_with()
        mock_input.assert_called_once()

    @mock.patch('banneret.main.input')
    def test_remove_everything_abort(self, mock_input, mock_clean_docker, args):
        args.containers, args.images, args.volumes = False, False, False
        mock_input.return_value = 'no'
        with pytest.raises(SystemExit):
            run_docker_command(args)
        mock_clean_docker.assert_not_called()
        mock_input.assert_called_once()


@mock.patch('banneret.main.input')
@mock.patch('banneret.main.enable_errors')
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

    def test_switch_for_all_abort(self, mock_enable_errors, mock_input, args):
        args.version = 'pycharm'
        mock_input.return_value = 'no'
        with pytest.raises(SystemExit):
            run_enable_errors_command(args)
        mock_enable_errors.assert_not_called()
        mock_input.assert_called_once()

    def test_no_settings_was_found(self, mock_enable_errors, mock_input, args):
        mock_enable_errors.side_effect = FileNotFoundError
        args.version = 'pycharm'
        mock_input.return_value = 'yes'
        with pytest.raises(SystemExit):
            run_enable_errors_command(args)
        mock_enable_errors.assert_called_once()
        mock_input.assert_called_once()
