import pytest

from banneret.main import enable_error, enable_errors


@pytest.fixture(name='mock_enable_error')
def fixture_enable_error(mocker):
    mock_enable_error = mocker.patch('banneret.main.enable_error')
    yield mock_enable_error


class TestEnableErrors:

    @pytest.mark.parametrize('disable', [True, False])
    def test_no_settings_dir(self, mock_enable_error, base_path, disable):
        with pytest.raises(IOError):
            enable_errors('PyCharm2017.1', path=base_path, disable=disable)
        mock_enable_error.assert_not_called()

    @pytest.mark.parametrize('disable', [True, False])
    def test_dir_exist(self, mock_enable_error, mocker, base_path, disable):
        for folder in ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']:
            base_path.mkdir(folder)
        enable_errors('PyCharm*', path=base_path, disable=disable)
        switch = 'disable' if disable else 'enable'
        calls = [mocker.call(base_path.join('PyCharm2016.3'), switch),
                 mocker.call(base_path.join('PyCharm2017.2'), switch),
                 mocker.call(base_path.join('PyCharmCE2017.2'), switch)]
        mock_enable_error.assert_has_calls(calls, any_order=True)


class TestEnableError:

    @staticmethod
    def create_file(path, content):
        with path.join('idea.properties').open('w') as config_file:
            config_file.write(content)

    @staticmethod
    def check_file(path, expected):
        with path.join('idea.properties').open('r') as config_file:
            assert config_file.read() == expected

    @pytest.mark.parametrize('switch', ['enable', 'disable'])
    def test_config_file_was_not_found(self, base_path, switch):
        config_line = 'idea.fatal.error.notification=%sd\n' % switch
        enable_error(base_path, switch)
        with base_path.join('idea.properties').open() as config_file:
            assert config_file.read() == config_line

    @pytest.mark.parametrize('switch', ['enable', 'disable'])
    def test_config_file_without_line(self, base_path, switch):
        self.create_file(base_path, 'first\nsecond\n')
        config_line = 'idea.fatal.error.notification=%sd\n' % switch
        enable_error(base_path, switch)
        self.check_file(base_path, 'first\nsecond\n' + config_line)

    def test_config_file_with_line_enable(self, base_path):
        self.create_file(base_path, 'idea.fatal.error.notification=enabled')
        config_line = 'idea.fatal.error.notification=disabled\n'
        enable_error(base_path, 'disable')
        self.check_file(base_path, config_line)

    def test_config_file_with_line_disable(self, base_path):
        self.create_file(base_path, 'idea.fatal.error.notification=disabled')
        config_line = 'idea.fatal.error.notification=enabled\n'
        enable_error(base_path, 'enable')
        self.check_file(base_path, config_line)

    @pytest.mark.parametrize('switch', ['enable', 'disable'])
    def test_nothing_to_change(self, base_path, switch):
        config_line = 'idea.fatal.error.notification=%sd' % switch
        self.create_file(base_path, config_line)
        with pytest.raises(SystemExit):
            enable_error(base_path, switch)
