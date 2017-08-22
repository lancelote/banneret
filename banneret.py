#!/usr/local/bin/python3
# v0.1.3

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


def purify(version=None):
    if not version:
        sure = input('are you sure you want to purify your system (yes/no)? ')
        if sure == 'yes':
            version = 'PyCharm*'
        else:
            print('abort')
            return

    if not sys.platform == 'darwin':
        print('only macOS is supported')

    configurations = glob(f'{CONFIGS}/{version}')
    caches = glob(f'{CACHES}/{version}')
    plugins = glob(f'{PLUGINS}/{version}')
    logs = glob(f'{LOGS}/{version}')

    print('removing configurations...')
    for config in configurations:
        print(f'    {config}')
        rmtree(config)

    print('removing caches...')
    for cache in caches:
        print(f'    {cache}')
        rmtree(cache)

    print('removing plugins...')
    for plugin in plugins:
        print(f'    {plugin}')
        rmtree(plugin)

    print('removing logs...')
    for log in logs:
        print(f'    {log}')
        rmtree(log)

    print('done')


def create_parser():
    parser = argparse.ArgumentParser(description='utils for PyCharm')
    commands = parser.add_subparsers(title='commands', dest='command')
    # commands.required = True

    # clean
    clean = commands.add_parser('clean', help='remove PyCharm configs')
    clean.add_argument(
        'version',
        type=str,
        help='IDE version to remove configs',
        nargs='?'
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'clean':
        purify(args)


if __name__ == '__main__':
    main()
