import pytest

from banneret.main import clean_docker, remove_containers, remove_images, \
    remove_volumes


@pytest.fixture(name='mock_remove_containers')
def fixture_mock_remove_containers(mocker):
    mock_remove_containers = mocker.patch('banneret.main.remove_containers')
    yield mock_remove_containers


@pytest.fixture(name='mock_remove_images')
def fixture_mock_remove_images(mocker):
    mock_remove_images = mocker.patch('banneret.main.remove_images')
    yield mock_remove_images


@pytest.fixture(name='mock_remove_volumes')
def fixture_mock_remove_volumes(mocker):
    mock_remove_volumes = mocker.patch('banneret.main.remove_volumes')
    yield mock_remove_volumes


class TestCleanDocker:

    def test_remove_everything(self,
                               mock_remove_containers,
                               mock_remove_images,
                               mock_remove_volumes):
        clean_docker()
        mock_remove_containers.assert_called_once()
        mock_remove_images.assert_called_once()
        mock_remove_volumes.assert_called_once()

    def test_remove_only_containers(self,
                                    mock_remove_containers,
                                    mock_remove_images,
                                    mock_remove_volumes):
        clean_docker(containers=True, images=False, volumes=False)
        mock_remove_containers.assert_called_once()
        mock_remove_images.assert_not_called()
        mock_remove_volumes.assert_not_called()

    def test_remove_only_images(self,
                                mock_remove_containers,
                                mock_remove_images,
                                mock_remove_volumes):
        clean_docker(containers=False, images=True, volumes=False)
        mock_remove_containers.assert_not_called()
        mock_remove_images.assert_called_once()
        mock_remove_volumes.assert_not_called()

    def test_remove_only_volumes(self,
                                 mock_remove_containers,
                                 mock_remove_images,
                                 mock_remove_volumes):
        clean_docker(containers=False, images=False, volumes=True)
        mock_remove_containers.assert_not_called()
        mock_remove_images.assert_not_called()
        mock_remove_volumes.assert_called_once()

    def test_remove_containers_and_volumes(self,
                                           mock_remove_containers,
                                           mock_remove_images,
                                           mock_remove_volumes):
        clean_docker(containers=True, images=False, volumes=True)
        mock_remove_containers.assert_called_once()
        mock_remove_images.assert_not_called()
        mock_remove_volumes.assert_called_once()

    def test_nothing_was_removed(self,
                                 mock_remove_containers,
                                 mock_remove_images,
                                 mock_remove_volumes):
        mock_remove_containers.return_value = False
        mock_remove_images.return_value = False
        mock_remove_volumes.return_value = False
        result = clean_docker()
        assert not result

    def test_everything_was_removed(self,
                                    mock_remove_containers,
                                    mock_remove_images,
                                    mock_remove_volumes):
        mock_remove_containers.return_value = True
        mock_remove_images.return_value = True
        mock_remove_volumes.return_value = True
        result = clean_docker()
        assert result

    def test_images_were_removed(self,
                                 mock_remove_containers,
                                 mock_remove_images,
                                 mock_remove_volumes):
        mock_remove_containers.return_value = False
        mock_remove_images.return_value = True
        mock_remove_volumes.return_value = False
        result = clean_docker()
        assert result


class TestRemoveContainers:

    def test_no_containers_are_available(self, client):
        client.containers.list.return_value = []
        result = remove_containers(client)
        assert not result

    def test_two_containers_are_available(self, client, mocker):
        container1 = mocker.Mock()
        container2 = mocker.Mock()
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

    def test_two_images_are_available(self, client, mocker):
        image1 = mocker.Mock()
        image2 = mocker.Mock()
        client.images.list.return_value = [image1, image2]
        result = remove_images(client)
        assert result
        calls = [mocker.call(image=image1.short_id, force=True),
                 mocker.call(image=image2.short_id, force=True)]
        client.images.remove.assert_has_calls(calls)


class TestRemoveVolumes:

    def test_no_volumes_are_available(self, client):
        client.volumes.list.return_value = []
        result = remove_volumes(client)
        assert not result

    def test_two_volumes_are_available(self, client, mocker):
        volume1 = mocker.Mock()
        volume2 = mocker.Mock()
        client.volumes.list.return_value = [volume1, volume2]
        result = remove_volumes(client)
        assert result
        volume1.remove.assert_called_once()
        volume2.remove_assert_called_once()
