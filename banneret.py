#!/usr/local/bin/python3

__version__ = '0.2.0'

import argparse
import re
import os
import sys
import getpass
from shutil import rmtree, make_archive
from glob import glob

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
        print('rm %s' % folder)
        rmtree(folder)
    return bool(folders)


def remove_all(configs=False, caches=False, plugins=False, logs=False,
               version='PyCharm*'):
    removed = False
    everything = True not in [configs, caches, plugins, logs]
    if not sys.platform == 'darwin':
        print('only macOS is supported')
        return

    if configs or everything:
        removed |= remove(CONFIGS, version)
    if caches or everything:
        removed |= remove(CACHES, version)
    if plugins or everything:
        removed |= remove(PLUGINS, version)
    if logs or everything:
        removed |= remove(LOGS, version)
    return removed


def archive_project(project, target, projects=PROJECTS):
    project, target, projects = str(project), str(target), str(projects)
    if os.sep not in project:
        project = os.path.join(projects, project)
    archive = os.path.join(target, project.split(os.sep)[-1])
    make_archive(base_name=archive, format='zip', root_dir=project)


def create_parser():
    parser = argparse.ArgumentParser(description='utils for PyCharm')
    commands = parser.add_subparsers(title='commands', dest='command')
    commands.required = True

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
    return parser


def normalize_version(version):
    match = re.match(r'(?P<ide>[a-zA-Z]+)(?P<version>[\d.]+)?', version)
    if not match or match.group('ide').lower() not in SUPPORTED_IDE:
        raise ValueError
    else:
        ide = SUPPORTED_IDE[match.group('ide').lower()]
        version = match.group('version') or '*'
        return ide, version


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'clean':
        try:
            ide, version = normalize_version(args.version)
        except ValueError:
            print('wrong or unsupported target')
            return
        if version != '*' or input('remove all versions? (yes/no) ') == 'yes':
            removed = remove_all(args.configs, args.caches, args.plugins,
                                 args.logs, ide + version)
            if not removed:
                print('nothing to remove')
        else:
            print('abort')
            return
    elif args.command == 'archive':
        archive_project(args.project, args.target)


if __name__ == '__main__':
    main()
