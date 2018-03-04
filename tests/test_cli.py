import pytest

from banneret.main import cli, PLATFORMS


class TestOSSupport:

    @pytest.mark.parametrize('platform', PLATFORMS)
    def test_support_os(self, log, runner, mocker, platform,
                        mock_archive_project):
        mocker.patch('sys.platform', platform)
        result = runner.invoke(cli, ['archive'])
        assert result.exit_code == 0
        assert 'Wrong os' not in log.text
        mock_archive_project.assert_called_once()

    def test_windows_is_not_supported(self, log, runner, mocker,
                                      mock_archive_project):
        mocker.patch('sys.platform', 'win32')
        result = runner.invoke(cli, ['archive'])
        assert result.exit_code == 1
        assert 'Wrong os: win32' in log.text
        mock_archive_project.assert_not_called()


class TestCLI:

    def test_clean(self, runner, mock_remove_all):
        runner.invoke(cli, ['clean', 'pycharm2017.1'], input='y\n')
        mock_remove_all.assert_called_once()

    def test_archive(self, runner, mock_archive_project):
        runner.invoke(cli, ['archive'])
        mock_archive_project.assert_called_once()

    def test_docker(self, runner, mock_clean_docker):
        runner.invoke(cli, ['docker'], input='y\n')
        mock_clean_docker.assert_called_once()

    def test_errors(self, runner, mock_enable_errors):
        runner.invoke(cli, ['errors', 'pycharm2017.1'])
        mock_enable_errors.assert_called_once()


class TestCleanCommand:

    def test_wrong_version(self, runner, log, mock_remove_all):
        result = runner.invoke(cli, ['clean', 'some_version'])
        assert result.exit_code == 1
        assert 'Wrong or unsupported version' in log.text
        mock_remove_all.assert_not_called()

    def test_correct_version(self, runner, mock_remove_all):
        result = runner.invoke(cli, ['clean', 'pycharm2017.2'])
        assert result.exit_code == 0
        mock_remove_all.assert_called_once()

    def test_remove_all(self, runner, mock_remove_all):
        result = runner.invoke(cli, ['clean', 'pycharm'], input='y\n')
        assert result.exit_code == 0
        mock_remove_all.assert_called_once()

    def test_remove_all_abort(self, runner, log, mock_remove_all):
        result = runner.invoke(cli, ['clean', 'pycharm'], input='N\n')
        assert result.exit_code == 1
        assert 'Abort' in log.text
        mock_remove_all.assert_not_called()

    def test_nothing_to_remove(self, runner, log, mock_remove_all):
        mock_remove_all.return_value = False
        result = runner.invoke(cli, ['clean', 'pycharm2017.2'])
        assert result.exit_code == 1
        assert 'Nothing to remove' in log.text
        mock_remove_all.assert_called_once()


class TestArchiveCommand:

    def test_wrong_target_or_project(self, runner, log, mock_archive_project):
        mock_archive_project.side_effect = IOError
        result = runner.invoke(cli, ['archive'])
        assert result.exit_code == 1
        assert 'Unknown project or target' in log.text
        mock_archive_project.assert_called_once()

    def test_correct_run(self, runner, mock_archive_project):
        result = runner.invoke(cli, ['archive'])
        assert result.exit_code == 0
        mock_archive_project.assert_called_once()


class TestDockerCommand:

    def test_no_docker(self, mocker, runner, log, mock_clean_docker):
        mocker.patch('banneret.main.docker_api', None)
        result = runner.invoke(cli, ['docker'])
        assert result.exit_code == 1
        assert 'Docker API SDK required' in log.text
        mock_clean_docker.assert_not_called()

    def test_remove_only_something(self, runner, mock_clean_docker):
        result = runner.invoke(cli, ['docker', '-i'])
        assert result.exit_code == 0
        mock_clean_docker.assert_called_with(False, True, False)

    def test_remove_everything(self, runner, mock_clean_docker):
        result = runner.invoke(cli, ['docker'], input='y\n')
        assert result.exit_code == 0
        mock_clean_docker.assert_called_with()

    def test_remove_all_abort(self, runner, log, mock_clean_docker):
        result = runner.invoke(cli, ['docker'], input='N\n')
        assert result.exit_code == 1
        assert 'Abort' in log.text
        mock_clean_docker.assert_not_called()

    def test_nothing_to_remove(self, runner, log, mock_clean_docker):
        mock_clean_docker.return_value = False
        result = runner.invoke(cli, ['docker'], input='y\n')
        assert result.exit_code == 1
        assert 'Nothing to remove' in log.text
        mock_clean_docker.assert_called_once()


class TestRunErrorsCommand:

    def test_wrong_version(self, runner, log, mock_enable_errors):
        result = runner.invoke(cli, ['errors', 'some_version'])
        assert result.exit_code == 1
        assert 'Wrong or unsupported version' in log.text
        mock_enable_errors.assert_not_called()

    def test_correct_version(self, runner, log, mock_enable_errors):
        result = runner.invoke(cli, ['errors', 'pycharm2017.3'])
        assert result.exit_code == 0
        assert 'Restart PyCharm to apply changes' in log.text
        mock_enable_errors.assert_called_once()

    def test_switch_for_all(self, runner, log, mock_enable_errors):
        result = runner.invoke(cli, ['errors', 'pycharm'], input='y\n')
        assert result.exit_code == 0
        assert 'Restart PyCharm to apply changes' in log.text
        mock_enable_errors.assert_called_once()

    def test_switch_for_all_abort(self, runner, log, mock_enable_errors):
        result = runner.invoke(cli, ['errors', 'pycharm'], input='N\n')
        assert result.exit_code == 1
        assert 'Abort' in log.text
        mock_enable_errors.assert_not_called()

    def test_no_settings_was_found(self, runner, log, mock_enable_errors):
        mock_enable_errors.side_effect = IOError
        result = runner.invoke(cli, ['errors', 'pycharm'], input='y\n')
        assert result.exit_code == 1
        assert 'No settings folder' in log.text
        mock_enable_errors.assert_called_once()
