"""Banneret main entry point."""

import logging
import sys

import click

from banneret import Banneret
from banneret.main import docker_api, PWD, DESKTOP
from banneret.version import __version__

PLATFORMS = {
    'darwin',
    'linux',
    'linux2',
}


@click.group()
@click.version_option(version=__version__)
@click.option('-v', '--verbose', is_flag=True, help='Enable debug logging.')
@click.pass_context
def cli(ctx, verbose):
    """Execute main entry point."""
    if sys.platform not in PLATFORMS:
        logging.info('Wrong os: %s', sys.platform)
        sys.exit(1)
    else:
        ctx.obj = Banneret()

    logging_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=logging_level, format='%(message)s')
    logging.debug('CLI arguments: %s', ', '.join(sys.argv[1:]))


@cli.command(help='Remove IDE settings.')
@click.argument('version')
@click.option('-s', '--configs', is_flag=True, help='Remove configurations.')
@click.option('-c', '--caches', is_flag=True, help='Remove caches.')
@click.option('-p', '--plugins', is_flag=True, help='Remove plugins.')
@click.option('-l', '--logs', is_flag=True, help='Remove logs.')
@click.pass_obj
def clean(bnrt, version, **kwargs):
    """Execute clean command for settings wipe."""
    try:
        ide, version = bnrt.normalize_version(version)
    except ValueError:
        logging.info('Wrong or unsupported version: %s', version)
        sys.exit(1)
    if version != '*' or click.confirm('Remove all versions?'):
        removed = bnrt.remove_all(ide + version, **kwargs)
        if not removed:
            logging.info('Nothing to remove')
            sys.exit(1)
    else:
        logging.info('Abort')
        sys.exit(1)


@cli.command(help='Archive current project.')
@click.option('-p', '--project', default=PWD)
@click.option('-t', '--target', default=DESKTOP)
@click.pass_obj
def archive(bnrt, project, target):
    """Execute archive command to backup project."""
    try:
        bnrt.archive_project(project, target)
    except IOError:
        logging.info('Unknown project or target')
        sys.exit(1)


@cli.command(help='Remove Docker artifacts.')
@click.option('-c', '--containers', is_flag=True, help='Remove containers.')
@click.option('-i', '--images', is_flag=True, help='Remove images.')
@click.option('-v', '--volumes', is_flag=True, help='Remove volumes.')
@click.pass_obj
def docker(bnrt, containers, images, volumes):
    """Execute docker command to remove docker-related objects."""
    if not docker_api:
        logging.info('Docker API SDK required to operate'
                     ' - pip install docker')
        sys.exit(1)
    elif containers or images or volumes:
        removed = bnrt.clean_docker(containers, images, volumes)
    elif click.confirm('Remove all containers/images/volumes?'):
        removed = bnrt.clean_docker()
    else:
        logging.info('Abort')
        sys.exit(1)
    if not removed:
        logging.info('Nothing to remove')
        sys.exit(1)


@cli.command(help='Enable notifications.')
@click.argument('version')
@click.option('-d', '--disable', )
@click.pass_obj
def errors(bnrt, version, disable):
    """Execute enable error command to switch IDE error notification."""
    try:
        ide, version = bnrt.normalize_version(version)
    except ValueError:
        logging.info('Wrong or unsupported version: %s', version)
        sys.exit(1)
    switch = 'disable' if disable else 'enable'
    answer = '{} for all versions?'.format(switch.capitalize())
    if version != '*' or click.confirm(answer):
        try:
            bnrt.enable_errors(version=ide + version, disable=disable)
            logging.info('Restart PyCharm to apply changes')
        except IOError:
            logging.info('No settings folder - try to start PyCharm once')
            sys.exit(1)
    else:
        logging.info('Abort')
        sys.exit(1)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
