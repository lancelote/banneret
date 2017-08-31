#!/usr/local/bin/python3
# v0.1.7

import argparse
import sys
import getpass
from shutil import rmtree
from glob import glob

USER = getpass.getuser()
HOME = f'/Users/{USER}'

CONFIGS = f'{HOME}/Library/Preferences'
CACHES = f'{HOME}/Library/Caches'
PLUGINS = f'{HOME}/Library/Application Support'
LOGS = f'{HOME}/Library/Logs'


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
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'clean':
        if args.version or input('remove for all versions? (yes/no) ') == 'yes':
            removed = remove_all(args.configs, args.caches, args.plugins,
                                 args.logs, args.version)
            if not removed:
                print('nothing to remove')
        else:
            print('abort')


if __name__ == '__main__':
    main()
