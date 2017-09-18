from unittest import mock
from unittest.mock import call
from os.path import join

import pytest

from banneret import enable_errors


@mock.patch('banneret.enable_error')
class TestEnableErrors:

    @pytest.mark.parametrize('disable', [True, False])
    def test_no_settings_folder(self, mock_enable_error, tmpdir, disable):
        base_path = tmpdir.mkdir('base_path')
        with pytest.raises(FileNotFoundError):
            enable_errors('PyCharm2017.1', path=base_path, disable=disable)
        mock_enable_error.assert_not_called()

    @pytest.mark.parametrize('disable', [True, False])
    def test_there_folders_to_apply(self, mock_enable_error, tmpdir, disable):
        base_path = tmpdir.mkdir('base_path')
        for folder in ['PyCharm2016.3', 'PyCharmCE2017.2', 'PyCharm2017.2']:
            base_path.mkdir(folder)
        enable_errors('PyCharm*', path=base_path, disable=disable)
        switch = 'disable' if disable else 'enable'
        calls = [call(join(base_path, 'PyCharm2016.3'), switch),
                 call(join(base_path, 'PyCharm2017.2'), switch),
                 call(join(base_path, 'PyCharmCE2017.2'), switch)]
        mock_enable_error.assert_has_calls(calls)
