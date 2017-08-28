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


def remove(version, path):
    folders = glob('%s/%s' % (path, version))
    for folder in folders:
        print('rm %s' % folder)
        rmtree(folder)


def remove_all(configs, caches, plugins, logs, version='PyCharm*'):
    everything = True not in [configs, caches, plugins, logs]
    if not sys.platform == 'darwin':
        print('only macOS is supported')
        return

    if configs or everything:
        remove(version, CONFIGS)
    if caches or everything:
        remove(version, CACHES)
    if plugins or everything:
        remove(version, PLUGINS)
    if logs or everything:
        remove(version, LOGS)

    print('done')


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
            remove_all(args.configs, args.caches, args.plugins, args.logs,
                       args.version)
        else:
            print('abort')


if __name__ == '__main__':
    main()
