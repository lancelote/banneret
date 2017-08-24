#!/usr/local/bin/python3
# v0.1.5

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


def clean_settings(args):
    version = args.version
    if not version:
        sure = input('purify settings for all versions? (yes/no) ')
        if sure == 'yes':
            version = 'PyCharm*'
        else:
            print('abort')
            return

    clean_all = False
    if not any([args.configs, args.caches, args.plugins, args.logs]):
        clean_all = True

    if not sys.platform == 'darwin':
        print('only macOS is supported')
        return

    if args.configs or clean_all:
        configurations = glob(f'{CONFIGS}/{version}')
        print('removing configurations...')
        for config in configurations:
            print(f'    {config}')
            rmtree(config)

    if args.caches or clean_all:
        caches = glob(f'{CACHES}/{version}')
        print('removing caches...')
        for cache in caches:
            print(f'    {cache}')
            rmtree(cache)

    if args.plugins or clean_all:
        plugins = glob(f'{PLUGINS}/{version}')
        print('removing plugins...')
        for plugin in plugins:
            print(f'    {plugin}')
            rmtree(plugin)

    if args.logs or clean_all:
        logs = glob(f'{LOGS}/{version}')
        print('removing logs...')
        for log in logs:
            print(f'    {log}')
            rmtree(log)

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
        clean_settings(args)


if __name__ == '__main__':
    main()
