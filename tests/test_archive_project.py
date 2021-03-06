from zipfile import ZipFile


def test_folder_is_correctly_archived(tmpdir, bnrt):
    project = tmpdir.mkdir('project')
    target = tmpdir.mkdir('target')
    unpack_target = tmpdir.mkdir('unpack_target')
    archive = target.join('project.zip')

    with project.join('sample.py').open('w'):
        bnrt.archive_project(project, target)
    with ZipFile(archive.strpath) as file_archive:
        file_archive.extractall(unpack_target.strpath)

    assert target.listdir() == [archive]
    assert unpack_target.listdir() == [unpack_target.join('sample.py')]


def test_only_project_name_is_passed(tmpdir, bnrt):
    projects = tmpdir.mkdir('projects')
    project = projects.mkdir('project')
    target = tmpdir.mkdir('target')
    unpack_target = tmpdir.mkdir('unpack_target')
    archive = target.join('project.zip')

    with project.join('sample.py').open('w'):
        bnrt.archive_project('project', target, projects)
    with ZipFile(archive.strpath) as file_archive:
        file_archive.extractall(unpack_target.strpath)

    assert target.listdir() == [archive]
    assert unpack_target.listdir() == [unpack_target.join('sample.py')]
