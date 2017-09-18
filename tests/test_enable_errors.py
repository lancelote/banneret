from unittest import mock
from unittest.mock import call
from os.path import join

import pytest

from banneret import enable_error, enable_errors


@mock.patch('banneret.enable_error')
class TestEnableErrors:

    @pytest.mark.parametrize('disable', [True, False])
    def test_no_settings_folder(self, mock_enable_error, base_path, disable):
        with pytest.raises(FileNotFoundError):
            enable_errors('PyCharm2017.1', path=base_path, disable=disable)
        mock_enable_error.assert_not_called()

    @pytest.mark.parametrize('disable', [True, False])
    def test_folders_exist(self, mock_enable_error, base_path, disable):
        for folder in ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']:
            base_path.mkdir(folder)
        enable_errors('PyCharm*', path=base_path, disable=disable)
        switch = 'disable' if disable else 'enable'
        calls = [call(join(base_path, 'PyCharm2016.3'), switch),
                 call(join(base_path, 'PyCharm2017.2'), switch),
                 call(join(base_path, 'PyCharmCE2017.2'), switch)]
        mock_enable_error.assert_has_calls(calls, any_order=True)


class TestEnableError:

    @staticmethod
    def create_file(path, content):
        with open(join(path, 'idea.properties'), 'w') as config_file:
            config_file.write(content)

    @staticmethod
    def check_file(path, expected):
        with open(join(path, 'idea.properties'), 'r') as config_file:
            assert config_file.read() == expected

    @pytest.mark.parametrize('switch', ['enable', 'disable'])
    def test_config_file_was_not_found(self, base_path, switch):
        config_line = 'idea.fatal.error.notification=%sd\n' % switch
        enable_error(base_path, switch)
        with open(join(base_path, 'idea.properties')) as config_file:
            assert config_file.read() == config_line

    @pytest.mark.parametrize('switch', ['enable', 'disable'])
    def test_config_file_without_line(self, base_path, switch):
        self.create_file(base_path, 'first\nsecond\n')
        config_line = 'idea.fatal.error.notification=%sd\n' % switch
        enable_error(base_path, switch)
        self.check_file(base_path, 'first\nsecond\n' + config_line)

    @pytest.mark.parametrize('switch', ['enable', 'disable'])
    def test_config_file_with_line_enable(self, base_path, switch):
        self.create_file(base_path, 'idea.fatal.error.notification=enabled')
        config_line = 'idea.fatal.error.notification=%sd\n' % switch
        enable_error(base_path, switch)
        self.check_file(base_path, config_line)

    @pytest.mark.parametrize('switch', ['enable', 'disable'])
    def test_config_file_with_line_disable(self, base_path, switch):
        self.create_file(base_path, 'idea.fatal.error.notification=disabled')
        config_line = 'idea.fatal.error.notification=%sd\n' % switch
        enable_error(base_path, switch)
        self.check_file(base_path, config_line)
