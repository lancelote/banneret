#!/usr/local/bin/python3

__version__ = '0.4.1'

import argparse
import getpass
import logging
import os
import re
import sys
from glob import glob
from shutil import rmtree, make_archive

try:
    import docker
except ImportError:
    docker = None

USER = getpass.getuser()
HOME = f'/Users/{USER}'
PWD = os.getcwd()

PROJECTS = f'{HOME}/PycharmProjects'
CONFIGS = f'{HOME}/Library/Preferences'
CACHES = f'{HOME}/Library/Caches'
PLUGINS = f'{HOME}/Library/Application Support'
LOGS = f'{HOME}/Library/Logs'

SUPPORTED_IDE = {
    'pycharm': 'PyCharm',
    'pycharmce': 'PyCharmCE',
    'intellijidea': 'IntelliJIdea',
    'idea': 'IntelliJIdea',
    'intellij': 'IntelliJIdea'
}


def remove(path, version):
    folders = glob('%s/%s' % (path, version))
    for folder in folders:
        logging.info('rm %s' % folder)
        rmtree(folder)
    return bool(folders)


def remove_all(version, configs=False, caches=False, plugins=False, logs=False):
    logging.debug('remove args: version %s, configs %s, caches %s, plugins %s, '
                  'logs %s' % (version, configs, caches, plugins, logs))
    removed = False
    everything = not any([configs, caches, plugins, logs])
    logging.debug('remove all settings: %s' % everything)
    if not sys.platform == 'darwin':
        logging.info('wrong os: %s' % sys.platform)
        return

    if configs or everything:
        removed |= remove(CONFIGS, version)
    if caches or everything:
        removed |= remove(CACHES, version)
    if plugins or everything:
        removed |= remove(PLUGINS, version)
    if logs or everything:
        removed |= remove(LOGS, version)
    logging.debug('was something removed: %s' % removed)
    return removed


def archive_project(project, target, projects=PROJECTS):
    logging.debug('archive: project %s to target %s' % (project, target))
    project, target, projects = str(project), str(target), str(projects)
    if os.sep not in project:
        project = os.path.join(projects, project)
        logging.debug('project path not found, new path: %s' % project)
    archive = os.path.join(target, project.split(os.sep)[-1])
    make_archive(base_name=archive, format='zip', root_dir=project)
    logging.info('archive %s.zip is created' % archive)


def normalize_version(version):
    logging.debug('normalize: version %s' % version)
    match = re.match(r'(?P<ide>[a-zA-Z]+)(?P<version>[\d.]+)?', version)
    if not match or match.group('ide').lower() not in SUPPORTED_IDE:
        raise ValueError
    else:
        ide = SUPPORTED_IDE[match.group('ide').lower()]
        version = match.group('version') or '*'
        logging.debug('normalize result: ide %s, version %s' % (ide, version))
        return ide, version


def remove_containers(client):
    containers = client.containers.list(all=True)
    for container in containers:
        logging.info('rm %s' % container)
        container.remove(force=True)
    return bool(containers)


def remove_images(client):
    images = client.images.list()
    for image in images:
        logging.info('rm %s' % images)
        client.images.remove(image=image.short_id, force=True)
    return bool(images)


def remove_volumes(client):
    volumes = client.volumes.list()
    for volume in volumes:
        logging.info('rm %s' % volume)
        volume.remove(force=True)
    return bool(volumes)


def clean_docker(containers=True, images=True, volumes=True):
    logging.debug('clean docker args: containers=%s, images=%s, volumes=%s'
                  % (containers, images, volumes))
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
    """switch exception notification for specific settings folder"""
    option = slice(0, 29)
    value = slice(30, None)
    config_file = os.path.join(folder, 'idea.properties')
    config_line = 'idea.fatal.error.notification=%sd\n' % switch
    try:
        with open(config_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        logging.debug('config file was not found')
        lines = [config_line]
    else:
        for i, line in enumerate(lines):
            if line[option] == 'idea.fatal.error.notification':
                if switch in line[value]:
                    logging.info('already %sd' % switch)
                    sys.exit(1)
                else:
                    logging.debug('config line was found')
                    lines[i] = config_line
                    break
        else:
            lines.append(config_line)
    with open(config_file, 'w') as f:
        logging.info('%s notifications in %s' % (switch, config_file))
        f.writelines(lines)


def enable_errors(version, path=CONFIGS, disable=False):
    """switch exception notification for given version"""
    switch = 'disable' if disable else 'enable'
    folders = glob('%s/%s' % (path, version))
    for folder in folders:
        enable_error(folder, switch)
    if not folders:
        raise FileNotFoundError


def create_parser():
    parser = argparse.ArgumentParser(description='utils for PyCharm')
    commands = parser.add_subparsers(title='commands', dest='command')
    commands.required = True

    # version
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)

    # verbose
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose level')

    # clean
    cmd_clean = commands.add_parser('clean', help='remove PyCharm settings')
    cmd_clean.add_argument('version', type=str,
                           help='IDE version to remove settings for')
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
    cmd_archive.add_argument('-t', '--target', default=f'{HOME}/Desktop',
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
    cmd_errors = commands.add_parser('errors', help='enable notifications')
    cmd_errors.add_argument('version', type=str,
                            help='IDE version to switch notifications')
    cmd_errors.add_argument('-d', '--disable', action='store_true',
                            help='disable errors notifications')
    return parser


def run_clean_command(args):
    try:
        ide, version = normalize_version(args.version)
    except ValueError:
        logging.info('wrong or unsupported version: %s' % args.version)
        sys.exit(1)
    if version != '*' or input('remove all versions? (yes/no) ') == 'yes':
        removed = remove_all(
            ide + version, args.configs, args.caches, args.plugins, args.logs)
        if not removed:
            logging.info('nothing to remove')
    else:
        logging.info('abort')
        sys.exit(1)


def run_archive_command(args):
    try:
        archive_project(args.project, args.target)
    except FileNotFoundError:
        logging.info('unknown project or target')
        sys.exit(1)


def run_docker_command(args):
    if not docker:
        logging.info('docker api sdk required to operate'
                     ' - pip install docker')
        sys.exit(1)
    elif args.containers or args.images or args.volumes:
        removed = clean_docker(args.containers, args.images, args.volumes)
    elif input('remove all containers/images/volumes? (yes/no) ') == 'yes':
        removed = clean_docker()
    else:
        logging.info('abort')
        sys.exit(1)
    if not removed:
        logging.info('nothing to remove')


def run_enable_errors_command(args):
    try:
        ide, version = normalize_version(args.version)
    except ValueError:
        logging.info('wrong or unsupported version: %s' % args.version)
        sys.exit(1)
    switch = 'disable' if args.disable else 'enable'
    if version != '*' or input(f'{switch} for all versions? (yes/no)') == 'yes':
        try:
            enable_errors(version=ide + version, disable=args.disable)
            logging.info('restart PyCharm to apply changes')
        except FileNotFoundError:
            logging.info('settings folder was not - try to start PyCharm once')
            sys.exit(1)
    else:
        logging.info('abort')
        sys.exit(1)


def main():
    parser = create_parser()
    args = parser.parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(message)s')
    logging.debug('cli arguments: %s' % ', '.join(sys.argv[1:]))

    if args.command == 'clean':
        run_clean_command(args)
    elif args.command == 'archive':
        run_archive_command(args)
    elif args.command == 'docker':
        run_docker_command(args)
    elif args.command == 'errors':
        run_enable_errors_command(args)
    else:
        logging.info('unknown command')
        sys.exit(1)


if __name__ == '__main__':
    main()
