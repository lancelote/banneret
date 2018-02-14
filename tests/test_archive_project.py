from os.path import join
from shutil import unpack_archive

from banneret.main import archive_project


def test_folder_is_correctly_archived(tmpdir):
    project = tmpdir.mkdir('project')
    target = tmpdir.mkdir('target')
    unpack_target = tmpdir.mkdir('unpack_target')
    archive = join(target, 'project.zip')
    with open(join(project, 'sample.py'), 'w'):
        pass

    archive_project(project, target)
    unpack_archive(archive, unpack_target, format='zip')

    assert target.listdir() == [archive]
    assert unpack_target.listdir() == [join(unpack_target, 'sample.py')]


def test_only_project_name_is_passed(tmpdir):
    projects = tmpdir.mkdir('projects')
    project = projects.mkdir('project')
    target = tmpdir.mkdir('target')
    unpack_target = tmpdir.mkdir('unpack_target')
    archive = join(target, 'project.zip')

    with open(join(project, 'sample.py'), 'w'):
        pass

    archive_project('project', target, projects)
    unpack_archive(archive, unpack_target, format='zip')

    assert target.listdir() == [archive]
    assert unpack_target.listdir() == [join(unpack_target, 'sample.py')]
