"""Banneret main entry point."""

import getpass
import logging
import os
import re
import sys
from glob import glob

import click

from shutil import rmtree, make_archive

from banneret.version import __version__

try:
    import docker as docker_api
except ImportError:
    docker_api = None

USER = getpass.getuser()
HOME = '/Users/{user}'.format(user=USER)
PWD = os.getcwd()
DESKTOP = '{home}/Desktop'.format(home=HOME)

PROJECTS = '{home}/PycharmProjects'.format(home=HOME)
CONFIGS = '{home}/Library/Preferences'.format(home=HOME)
CACHES = '{home}/Library/Caches'.format(home=HOME)
PLUGINS = '{home}/Library/Application Support'.format(home=HOME)
LOGS = '{home}/Library/Logs'.format(home=HOME)

SUPPORTED_IDE_ALIASES = {
    'pycharm': 'PyCharm',
    'pycharmce': 'PyCharmCE',
    'intellijidea': 'IntelliJIdea',
    'idea': 'IntelliJIdea',
    'intellij': 'IntelliJIdea',
    'ideac': 'IdeaIC',
    'ideaic': 'IdeaIC',
}


def remove(path, version):
    """Remove all version folders from path."""
    path = str(path)
    folders = glob('%s/%s' % (path, version))
    for folder in folders:
        logging.info('rm %s', folder)
        rmtree(folder)
    return bool(folders)


def remove_all(version, configs=False, caches=False, plugins=False,
               logs=False):
    """Remove given settings for given IDE version."""
    logging.debug('Remove args: version %s, configs %s, caches %s, plugins %s,'
                  ' logs %s', version, configs, caches, plugins, logs)
    removed = False
    everything = not any([configs, caches, plugins, logs])
    logging.debug('Remove all settings: %s', everything)

    if configs or everything:
        removed |= remove(CONFIGS, version)
    if caches or everything:
        removed |= remove(CACHES, version)
    if plugins or everything:
        removed |= remove(PLUGINS, version)
    if logs or everything:
        removed |= remove(LOGS, version)
    logging.debug('Was something removed: %s', removed)
    return removed


def archive_project(project, target, projects=PROJECTS):
    """Archive given project and send to target."""
    logging.debug('archive: project %s to target %s', project, target)
    project, target, projects = str(project), str(target), str(projects)
    if os.sep not in project:
        project = os.path.join(projects, project)
        logging.debug('Project path not found, new path: %s', project)
    archive_path = os.path.join(target, project.split(os.sep)[-1])
    make_archive(base_name=archive_path, format='zip', root_dir=project)
    logging.info('Archive %s.zip is created', archive_path)


def normalize_version(version):
    """Convert user given IDE version to standard format."""
    logging.debug('Normalize: version %s', version)
    match = re.match(r'(?P<ide>[a-zA-Z]+)(?P<version>[\d.]+)?', version)
    if not match or match.group('ide').lower() not in SUPPORTED_IDE_ALIASES:
        raise ValueError
    else:
        ide = SUPPORTED_IDE_ALIASES[match.group('ide').lower()]
        version = match.group('version') or '*'
        logging.debug('Normalize result: ide %s, version %s', ide, version)
        return ide, version


def remove_containers(client):
    """Remove all docker containers."""
    containers = client.containers.list(all=True)
    for container in containers:
        logging.info('rm %s', container)
        container.remove(force=True)
    return bool(containers)


def remove_images(client):
    """Remove all docker images."""
    images = client.images.list()
    for image in images:
        logging.info('rm %s', image)
        client.images.remove(image=image.short_id, force=True)
    return bool(images)


def remove_volumes(client):
    """Remove all docker volumes."""
    volumes = client.volumes.list()
    for volume in volumes:
        logging.info('rm %s', volume)
        volume.remove(force=True)
    return bool(volumes)


def clean_docker(containers=True, images=True, volumes=True):
    """Remove given docker objects from system."""
    logging.debug('Clean docker args: containers=%s, images=%s, volumes=%s',
                  containers, images, volumes)
    removed = False
    client = docker_api.from_env()

    if containers:
        removed |= remove_containers(client)
    if images:
        removed |= remove_images(client)
    if volumes:
        removed |= remove_volumes(client)
    return removed


def enable_error(folder, switch):
    """Switch exception notification for specific settings folder."""
    folder = str(folder)
    option = slice(0, 29)
    value = slice(30, None)
    config_file = os.path.join(folder, 'idea.properties')
    config_line = 'idea.fatal.error.notification=%sd\n' % switch
    try:
        with open(config_file, 'r') as idea_properties:
            lines = idea_properties.readlines()
    except IOError:
        logging.debug('Config file was not found')
        lines = [config_line]
    else:
        for i, line in enumerate(lines):
            if line[option] == 'idea.fatal.error.notification':
                if switch in line[value]:
                    logging.info('Already %sd', switch)
                    sys.exit(1)
                else:
                    logging.debug('Config line was found')
                    lines[i] = config_line
                    break
        else:
            lines.append(config_line)
    with open(config_file, 'w') as idea_properties:
        logging.info('Notifications %sd for %s', switch, config_file)
        idea_properties.writelines(lines)


def enable_errors(version, path=CONFIGS, disable=False):
    """Switch exception notification for given version."""
    path = str(path)
    switch = 'disable' if disable else 'enable'
    folders = glob('%s/%s' % (path, version))
    for folder in folders:
        enable_error(folder, switch)
    if not folders:
        raise IOError


@click.group()
@click.version_option(version=__version__)
@click.option('-v', '--verbose', is_flag=True, help='Enable debug logging.')
def cli(verbose):
    """Execute main entry point."""
    if sys.platform != 'darwin':
        logging.info('Wrong os: %s', sys.platform)
        sys.exit(1)

    logging_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(message)s')
    logging.debug('CLI arguments: %s', ', '.join(sys.argv[1:]))


@cli.command(help='Remove IDE settings.')
@click.argument('version')
@click.option('-s', '--configs', is_flag=True, help='Remove configurations.')
@click.option('-c', '--caches', is_flag=True, help='Remove caches.')
@click.option('-p', '--plugins', is_flag=True, help='Remove plugins.')
@click.option('-l', '--logs', is_flag=True, help='Remove logs.')
def clean(version, configs, caches, plugins, logs):
    """Execute clean command for settings wipe."""
    try:
        ide, version = normalize_version(version)
    except ValueError:
        logging.info('Wrong or unsupported version: %s', version)
        sys.exit(1)
    if version != '*' or click.confirm('Remove all versions?'):
        removed = remove_all(ide + version, configs, caches, plugins, logs)
        if not removed:
            logging.info('Nothing to remove')
            sys.exit(1)
    else:
        logging.info('Abort')
        sys.exit(1)


@cli.command(help='Archive current project.')
@click.option('-p', '--project', default=PWD)
@click.option('-t', '--target', type=click.Path(exists=True), default=DESKTOP)
def archive(project, target):
    """Execute archive command to backup project."""
    try:
        archive_project(project, target)
    except IOError:
        logging.info('Unknown project or target')
        sys.exit(1)


@cli.command(help='Remove Docker artifacts.')
@click.option('-c', '--containers', is_flag=True, help='Remove containers.')
@click.option('-i', '--images', is_flag=True, help='Remove images.')
@click.option('-v', '--volumes', is_flag=True, help='Remove volumes.')
def docker(containers, images, volumes):
    """Execute docker command to remove docker-related objects."""
    if not docker_api:
        logging.info('Docker API SDK required to operate'
                     ' - pip install docker')
        sys.exit(1)
    elif containers or images or volumes:
        removed = clean_docker(containers, images, volumes)
    elif click.confirm('Remove all containers/images/volumes?'):
        removed = clean_docker()
    else:
        logging.info('Abort')
        sys.exit(1)
    if not removed:
        logging.info('Nothing to remove')
        sys.exit(1)


@cli.command(help='Enable notifications.')
@click.argument('version')
@click.option('-d', '--disable', )
def errors(version, disable):
    """Execute enable error command to switch IDE error notification."""
    try:
        ide, version = normalize_version(version)
    except ValueError:
        logging.info('Wrong or unsupported version: %s', version)
        sys.exit(1)
    switch = 'disable' if disable else 'enable'
    answer = '{} for all versions?'.format(switch.capitalize())
    if version != '*' or click.confirm(answer):
        try:
            enable_errors(version=ide + version, disable=disable)
            logging.info('Restart PyCharm to apply changes')
        except IOError:
            logging.info('No settings folder - try to start PyCharm once')
            sys.exit(1)
    else:
        logging.info('Abort')
        sys.exit(1)
