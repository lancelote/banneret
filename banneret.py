#!/usr/local/bin/python3

__version__ = '0.2.3'

import argparse
import getpass
import logging
import os
import re
import sys
from glob import glob
from shutil import rmtree, make_archive

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


def remove_all(configs=False, caches=False, plugins=False, logs=False,
               version='PyCharm*'):
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
    clean = commands.add_parser('clean', help='remove PyCharm settings')
    clean.add_argument('version', type=str, nargs='?',
                       help='IDE version to remove settings for')
    clean.add_argument('-C', '--configs', action='store_true',
                       help='remove configurations')
    clean.add_argument('-c', '--caches', action='store_true',
                       help='remove caches')
    clean.add_argument('-p', '--plugins', action='store_true',
                       help='remove plugins')
    clean.add_argument('-l', '--logs', action='store_true',
                       help='remove logs')

    # archive
    archive = commands.add_parser('archive', help='archive current project')
    archive.add_argument('-p', '--project', default=PWD,
                         help='project to be archived')
    archive.add_argument('-t', '--target', default=f'{HOME}/Desktop',
                         help='where archive will be placed')

    # docker
    docker = commands.add_parser('docker', help='removes docker artifacts')
    docker.add_argument('-v', '--volumes', action='store_true',
                        help='remove volumes')
    docker.add_argument('-c', '--containers', action='store_true',
                        help='remove containers')
    docker.add_argument('-i', '--images', action='store_true',
                        help='remove images')
    return parser


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


def clean_docker(volumes, containers, images):
    pass


def main():
    parser = create_parser()
    args = parser.parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(message)s')
    logging.debug('cli arguments: %s' % ', '.join(sys.argv[1:]))

    if args.command == 'clean':
        try:
            ide, version = normalize_version(args.version)
        except ValueError:
            logging.info('wrong or unsupported version: %s' % args.version)
            return
        if version != '*' or input('remove all versions? (yes/no) ') == 'yes':
            removed = remove_all(args.configs, args.caches, args.plugins,
                                 args.logs, ide + version)
            if not removed:
                logging.info('nothing to remove')
        else:
            logging.info('abort')
            return
    elif args.command == 'archive':
        try:
            archive_project(args.project, args.target)
        except FileNotFoundError:
            logging.info('unknown project or target')
            return
    elif args.command == 'docker':
        if args.volumes or args.containers or args.images:
            clean_docker(args.volumes, args.containers, args.images)
        else:
            clean_docker(True, True, True)


if __name__ == '__main__':
    main()
