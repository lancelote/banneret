"""Banneret main entry point."""

import argparse
import getpass
import logging
import sys
from glob import glob

import os
import re
from shutil import rmtree, make_archive

from banneret.version import __version__

try:
    import docker
except ImportError:
    docker = None

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


def remove_all(version, configs=False, caches=False, plugins=False, logs=False):
    """Remove given settings for given IDE version."""
    logging.debug('Remove args: version %s, configs %s, caches %s, plugins %s, '
                  'logs %s', version, configs, caches, plugins, logs)
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
    archive = os.path.join(target, project.split(os.sep)[-1])
    make_archive(base_name=archive, format='zip', root_dir=project)
    logging.info('Archive %s.zip is created', archive)


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
    client = docker.from_env()

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


def run_clean_command(args):
    """Execute clean command for settings wipe."""
    try:
        ide, version = normalize_version(args.version)
    except ValueError:
        logging.info('Wrong or unsupported version: %s', args.version)
        sys.exit(1)
    if version != '*' or input('Remove all versions? (yes/no) ') == 'yes':
        removed = remove_all(
            ide + version, args.configs, args.caches, args.plugins, args.logs)
        if not removed:
            logging.info('Nothing to remove')
            sys.exit(1)
    else:
        logging.info('Abort')
        sys.exit(1)


def run_archive_command(args):
    """Execute archive command to backup project."""
    try:
        archive_project(args.project, args.target)
    except IOError:
        logging.info('Unknown project or target')
        sys.exit(1)


def run_docker_command(args):
    """Execute docker command to remove docker-related objects."""
    if not docker:
        logging.info('Docker api sdk required to operate'
                     ' - pip install docker')
        sys.exit(1)
    elif args.containers or args.images or args.volumes:
        removed = clean_docker(args.containers, args.images, args.volumes)
    elif input('Remove all containers/images/volumes? (yes/no) ') == 'yes':
        removed = clean_docker()
    else:
        logging.info('Abort')
        sys.exit(1)
    if not removed:
        logging.info('Nothing to remove')


def run_enable_errors_command(args):
    """Execute enable error command to switch IDE error notification."""
    try:
        ide, version = normalize_version(args.version)
    except ValueError:
        logging.info('Wrong or unsupported version: %s', args.version)
        sys.exit(1)
    switch = 'disable' if args.disable else 'enable'
    answer = '{} for all versions? (yes/no)'.format(switch.capitalize())
    if version != '*' or input(answer) == 'yes':
        try:
            enable_errors(version=ide + version, disable=args.disable)
            logging.info('Restart PyCharm to apply changes')
        except IOError:
            logging.info('No settings folder - try to start PyCharm once')
            sys.exit(1)
    else:
        logging.info('Abort')
        sys.exit(1)


def create_parser():
    """CLI parser."""
    parser = argparse.ArgumentParser(description='Utils for PyCharm')
    commands = parser.add_subparsers(title='commands', dest='command')
    commands.required = True

    # parent parsers
    # ide version
    ide_version = argparse.ArgumentParser(add_help=False)
    ide_version.add_argument('version', type=str,
                             help='IDE version to remove settings for')

    # version
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)

    # verbose
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose level')

    # clean
    cmd_clean = commands.add_parser('clean', parents=[ide_version],
                                    help='remove PyCharm settings')
    cmd_clean.add_argument('-C', '--configs', action='store_true',
                           help='remove configurations')
    cmd_clean.add_argument('-c', '--caches', action='store_true',
                           help='remove caches')
    cmd_clean.add_argument('-p', '--plugins', action='store_true',
                           help='remove plugins')
    cmd_clean.add_argument('-l', '--logs', action='store_true',
                           help='remove logs')

    # archive
    cmd_archive = commands.add_parser('archive', help='archive current project')
    cmd_archive.add_argument('-p', '--project', default=PWD,
                             help='project to be archived')
    cmd_archive.add_argument('-t', '--target', default=DESKTOP,
                             help='where archive will be placed')

    # docker
    cmd_docker = commands.add_parser('docker', help='removes docker artifacts')
    cmd_docker.add_argument('-c', '--containers', action='store_true',
                            help='remove containers')
    cmd_docker.add_argument('-i', '--images', action='store_true',
                            help='remove images')
    cmd_docker.add_argument('-v', '--volumes', action='store_true',
                            help='remove volumes')

    # errors
    cmd_errors = commands.add_parser('errors', parents=[ide_version],
                                     help='enable notifications')
    cmd_errors.add_argument('-d', '--disable', action='store_true',
                            help='disable errors notifications')
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(message)s')
    logging.debug('CLI arguments: %s', ', '.join(sys.argv[1:]))

    if sys.platform != 'darwin':
        logging.info('Wrong os: %s', sys.platform)
        sys.exit(1)

    if args.command == 'clean':
        run_clean_command(args)
    elif args.command == 'archive':
        run_archive_command(args)
    elif args.command == 'docker':
        run_docker_command(args)
    elif args.command == 'errors':
        run_enable_errors_command(args)
    else:
        logging.info('Unknown command')
        sys.exit(1)


if __name__ == '__main__':
    main()
