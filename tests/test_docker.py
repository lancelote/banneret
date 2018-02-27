class TestCleanDocker:

    def test_remove_everything(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        bnrt.clean_docker()
        mock_remove_containers.assert_called_once()
        mock_remove_images.assert_called_once()
        mock_remove_volumes.assert_called_once()

    def test_remove_only_containers(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        bnrt.clean_docker(containers=True, images=False, volumes=False)
        mock_remove_containers.assert_called_once()
        mock_remove_images.assert_not_called()
        mock_remove_volumes.assert_not_called()

    def test_remove_only_images(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        bnrt.clean_docker(containers=False, images=True, volumes=False)
        mock_remove_containers.assert_not_called()
        mock_remove_images.assert_called_once()
        mock_remove_volumes.assert_not_called()

    def test_remove_only_volumes(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        bnrt.clean_docker(containers=False, images=False, volumes=True)
        mock_remove_containers.assert_not_called()
        mock_remove_images.assert_not_called()
        mock_remove_volumes.assert_called_once()

    def test_remove_containers_and_volumes(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        bnrt.clean_docker(containers=True, images=False, volumes=True)
        mock_remove_containers.assert_called_once()
        mock_remove_images.assert_not_called()
        mock_remove_volumes.assert_called_once()

    def test_nothing_was_removed(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        mock_remove_containers.return_value = False
        mock_remove_images.return_value = False
        mock_remove_volumes.return_value = False
        result = bnrt.clean_docker()
        assert not result

    def test_everything_was_removed(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        mock_remove_containers.return_value = True
        mock_remove_images.return_value = True
        mock_remove_volumes.return_value = True
        result = bnrt.clean_docker()
        assert result

    def test_images_were_removed(
            self,
            bnrt,
            mock_remove_containers,
            mock_remove_images,
            mock_remove_volumes
    ):
        mock_remove_containers.return_value = False
        mock_remove_images.return_value = True
        mock_remove_volumes.return_value = False
        result = bnrt.clean_docker()
        assert result


class TestRemoveContainers:

    def test_no_containers_are_available(self, docker_daemon, mocker):
        docker_client = mocker.patch.object(docker_daemon, 'client')
        docker_client.containers.list.return_value = []

        result = docker_daemon.remove_containers()
        assert not result

    def test_two_containers_are_available(self, docker_daemon, mocker):
        container1 = mocker.Mock()
        container2 = mocker.Mock()
        docker_client = mocker.patch.object(docker_daemon, 'client')
        docker_client.containers.list.return_value = [container1, container2]

        result = docker_daemon.remove_containers()
        assert result
        container1.remove.assert_called_once()
        container2.remove.assert_called_once()


class TestRemoveImages:

    def test_no_images_are_available(self, docker_daemon, mocker):
        docker_client = mocker.patch.object(docker_daemon, 'client')
        docker_client.images.list.return_value = []

        result = docker_daemon.remove_images()
        assert not result

    def test_two_images_are_available(self, docker_daemon, mocker):
        image1 = mocker.Mock()
        image2 = mocker.Mock()
        docker_client = mocker.patch.object(docker_daemon, 'client')
        docker_client.images.list.return_value = [image1, image2]

        result = docker_daemon.remove_images()
        assert result
        calls = [mocker.call(image=image1.short_id, force=True),
                 mocker.call(image=image2.short_id, force=True)]
        docker_client.images.remove.assert_has_calls(calls)


class TestRemoveVolumes:

    def test_no_volumes_are_available(self, docker_daemon, mocker):
        docker_client = mocker.patch.object(docker_daemon, 'client')
        docker_client.volumes.list.return_value = []

        result = docker_daemon.remove_volumes()
        assert not result

    def test_two_volumes_are_available(self, docker_daemon, mocker):
        volume1 = mocker.Mock()
        volume2 = mocker.Mock()
        docker_client = mocker.patch.object(docker_daemon, 'client')
        docker_client.volumes.list.return_value = [volume1, volume2]

        result = docker_daemon.remove_volumes()
        assert result
        volume1.remove.assert_called_once()
        volume2.remove_assert_called_once()
