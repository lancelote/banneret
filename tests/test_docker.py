from unittest import mock
from unittest.mock import call

from banneret import clean_docker, remove_containers, remove_images, \
    remove_volumes


@mock.patch('banneret.remove_volumes')
@mock.patch('banneret.remove_images')
@mock.patch('banneret.remove_containers')
class TestCleanDocker:

    def test_remove_everything(self, mock_rc, mock_ri, mock_rv):
        clean_docker()
        mock_rc.assert_called_once()
        mock_ri.assert_called_once()
        mock_rv.assert_called_once()

    def test_remove_only_containers(self, mock_rc, mock_ri, mock_rv):
        clean_docker(containers=True, images=False, volumes=False)
        mock_rc.assert_called_once()
        mock_ri.assert_not_called()
        mock_rv.assert_not_called()

    def test_remove_only_images(self, mock_rc, mock_ri, mock_rv):
        clean_docker(containers=False, images=True, volumes=False)
        mock_rc.assert_not_called()
        mock_ri.assert_called_once()
        mock_rv.assert_not_called()

    def test_remove_only_volumes(self, mock_rc, mock_ri, mock_rv):
        clean_docker(containers=False, images=False, volumes=True)
        mock_rc.assert_not_called()
        mock_ri.assert_not_called()
        mock_rv.assert_called_once()

    def test_remove_containers_and_volumes(self, mock_rc, mock_ri, mock_rv):
        clean_docker(containers=True, images=False, volumes=True)
        mock_rc.assert_called_once()
        mock_ri.assert_not_called()
        mock_rv.assert_called_once()

    def test_nothing_was_removed(self, mock_rc, mock_ri, mock_rv):
        mock_rc.return_value = False
        mock_ri.return_value = False
        mock_rv.return_value = False
        result = clean_docker()
        assert not result

    def test_everything_was_removed(self, mock_rc, mock_ri, mock_rv):
        mock_rc.return_value = True
        mock_ri.return_value = True
        mock_rv.return_value = True
        result = clean_docker()
        assert result

    def test_images_were_removed(self, mock_rc, mock_ri, mock_rv):
        mock_rc.return_value = False
        mock_ri.return_value = True
        mock_rv.return_value = False
        result = clean_docker()
        assert result


class TestRemoveContainers:

    def test_no_containers_are_available(self, client):
        client.containers.list.return_value = []
        result = remove_containers(client)
        assert not result

    def test_two_containers_are_available(self, client):
        container1 = mock.Mock()
        container2 = mock.Mock()
        client.containers.list.return_value = [container1, container2]
        result = remove_containers(client)
        assert result
        container1.remove.assert_called_once()
        container2.remove.assert_called_once()


class TestRemoveImages:

    def test_no_images_are_available(self, client):
        client.images.list.return_value = []
        result = remove_images(client)
        assert not result

    def test_two_images_are_available(self, client):
        image1 = mock.Mock()
        image2 = mock.Mock()
        client.images.list.return_value = [image1, image2]
        result = remove_images(client)
        assert result
        calls = [call(image=image1.short_id, force=True),
                 call(image=image2.short_id, force=True)]
        client.images.remove.assert_has_calls(calls)


class TestRemoveVolumes:

    def test_no_volumes_are_available(self, client):
        client.volumes.list.return_value = []
        result = remove_volumes(client)
        assert not result

    def test_two_volumes_are_available(self, client):
        volume1 = mock.Mock()
        volume2 = mock.Mock()
        client.volumes.list.return_value = [volume1, volume2]
        result = remove_volumes(client)
        assert result
        volume1.remove.assert_called_once()
        volume2.remove_assert_called_once()
