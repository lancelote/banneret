"""Banneret main entry point."""

import getpass
import logging
import os
import re
import sys
from glob import glob
from shutil import rmtree, make_archive

import click

from banneret.version import __version__

try:
    import docker as docker_api
except ImportError:
    docker_api = None


class BanneretMacOS:
    """Main application logic for macOS."""

    USER = getpass.getuser()
    HOME = '/Users/{user}'.format(user=USER)
    PWD = os.getcwd()
    DESKTOP = '{home}/Desktop'.format(home=HOME)
    PROJECTS = '{home}/PycharmProjects'.format(home=HOME)
    CONFIGS = '{home}/Library/Preferences'.format(home=HOME)
    CACHES = '{home}/Library/Caches'.format(home=HOME)
    PLUGINS = '{home}/Library/Application Support'.format(home=HOME)
    LOGS = '{home}/Library/Logs'.format(home=HOME)
    ALIASES = {
        'pycharm': 'PyCharm',
        'pycharmce': 'PyCharmCE',
        'intellijidea': 'IntelliJIdea',
        'idea': 'IntelliJIdea',
        'intellij': 'IntelliJIdea',
        'ideac': 'IdeaIC',
        'ideaic': 'IdeaIC',
    }

    @classmethod
    def default_project(cls):
        """Get default project path for archive command."""
        return cls.PWD

    @classmethod
    def default_target(cls):
        """Get default target path for archive command."""
        return cls.DESKTOP

    @staticmethod
    def remove(path, version):
        """Remove all version folders from path."""
        path = str(path)
        folders = glob('%s/%s' % (path, version))
        for folder in folders:
            logging.info('rm %s', folder)
            rmtree(folder)
        return bool(folders)

    def remove_all(self, version, **kwargs):
        """Remove given settings for given IDE version."""
        logging.debug('Remove args: version %s, %s', version, **kwargs)
        removed = False
        everything = not any(kwargs.values())
        configs = kwargs.get('configs', False)
        caches = kwargs.get('caches', False)
        plugins = kwargs.get('plugins', False)
        logs = kwargs.get('logs', False)
        logging.debug('Remove all settings: %s', everything)

        if configs or everything:
            removed |= self.remove(self.CONFIGS, version)
        if caches or everything:
            removed |= self.remove(self.CACHES, version)
        if plugins or everything:
            removed |= self.remove(self.PLUGINS, version)
        if logs or everything:
            removed |= self.remove(self.LOGS, version)
        logging.debug('Was something removed: %s', removed)
        return removed

    @staticmethod
    def archive_project(project=PWD, target=DESKTOP, projects=PROJECTS):
        """Archive given project and send to target."""
        logging.debug('archive: project %s to target %s', project, target)
        project, target, projects = str(project), str(target), str(projects)
        if os.sep not in project:
            project = os.path.join(projects, project)
            logging.debug('Project path not found, new path: %s', project)
        archive_path = os.path.join(target, project.split(os.sep)[-1])
        make_archive(base_name=archive_path, format='zip', root_dir=project)
        logging.info('Archive %s.zip is created', archive_path)

    def normalize_version(self, version):
        """Convert user given IDE version to standard format."""
        logging.debug('Normalize: version %s', version)
        match = re.match(r'(?P<ide>[a-zA-Z]+)(?P<version>[\d.]+)?', version)
        if not match or match.group('ide').lower() not in self.ALIASES:
            raise ValueError
        else:
            ide = self.ALIASES[match.group('ide').lower()]
            version = match.group('version') or '*'
            logging.debug('Normalize result: ide %s, version %s', ide, version)
            return ide, version

    @staticmethod
    def clean_docker(containers=True, images=True, volumes=True):
        """Remove given docker objects from system."""
        logging.debug('Clean docker: containers=%s, images=%s, volumes=%s',
                      containers, images, volumes)
        removed = False
        docker_client = Docker()

        if containers:
            removed |= docker_client.remove_containers()
        if images:
            removed |= docker_client.remove_images()
        if volumes:
            removed |= docker_client.remove_volumes()
        return removed

    @staticmethod
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

    def enable_errors(self, version, path=CONFIGS, disable=False):
        """Switch exception notification for given version."""
        path = str(path)
        switch = 'disable' if disable else 'enable'
        folders = glob('%s/%s' % (path, version))
        for folder in folders:
            self.enable_error(folder, switch)
        if not folders:
            raise IOError


class BanneretLinux(BanneretMacOS):
    pass


class Docker:
    """Main docker related application logic."""

    def __init__(self):
        """Create Docker API wrapper."""
        self.client = docker_api.from_env()

    def remove_containers(self):
        """Remove all docker containers."""
        containers = self.client.containers.list(all=True)
        for container in containers:
            logging.info('rm %s', container)
            container.remove(force=True)
        return bool(containers)

    def remove_images(self):
        """Remove all docker images."""
        images = self.client.images.list()
        for image in images:
            logging.info('rm %s', image)
            self.client.images.remove(image=image.short_id, force=True)
        return bool(images)

    def remove_volumes(self):
        """Remove all docker volumes."""
        volumes = self.client.volumes.list()
        for volume in volumes:
            logging.info('rm %s', volume)
            volume.remove(force=True)
        return bool(volumes)


@click.group()
@click.version_option(version=__version__)
@click.option('-v', '--verbose', is_flag=True, help='Enable debug logging.')
@click.pass_context
def cli(ctx, verbose):
    """Execute main entry point."""
    if sys.platform == 'darwin':
        ctx.obj = BanneretMacOS()
    elif sys.platform == 'linux':
        ctx.obj = BanneretLinux()
    else:
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
@click.option('-p', '--project', default=BanneretMacOS.default_project)
@click.option('-t', '--target', default=BanneretMacOS.default_target())
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
