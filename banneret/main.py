"""Main application logic."""

import getpass
import logging
import os
import re
import sys
from glob import glob
from shutil import rmtree, make_archive

try:
    import docker as docker_api
except ImportError:
    docker_api = None

ALIASES = {
    'pycharm': 'PyCharm',
    'pycharmce': 'PyCharmCE',
    'intellijidea': 'IntelliJIdea',
    'idea': 'IntelliJIdea',
    'intellij': 'IntelliJIdea',
    'ideac': 'IdeaIC',
    'ideaic': 'IdeaIC',
}

USER = getpass.getuser()
PWD = os.getcwd()

if sys.platform == 'darwin':
    HOME = '/Users/{user}'.format(user=USER)
    CONFIGS = '{home}/Library/Preferences'.format(home=HOME)
    CACHES = '{home}/Library/Caches'.format(home=HOME)
    PLUGINS = '{home}/Library/Application Support'.format(home=HOME)
    LOGS = '{home}/Library/Logs'.format(home=HOME)
elif sys.platform.startswith('linux'):
    HOME = '/home/{user}'.format(user=USER)
    CONFIGS = '{home}/{{version}}/config'.format(home=HOME)
    CACHES = '{home}/{{version}}/system/caches'.format(home=HOME)
    PLUGINS = '{home}/{{version}}/config/plugins'.format(home=HOME)
    LOGS = '{home}/{{version}}/system/log'.format(home=HOME)
else:
    HOME = None
    CONFIGS = None
    CACHES = None
    PLUGINS = None
    LOGS = None

DESKTOP = '{home}/Desktop'.format(home=HOME)
PROJECTS = '{home}/PycharmProjects'.format(home=HOME)


class BanneretMacOS(object):
    """Main application logic for macOS."""

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
        removed = False
        everything = not any(kwargs.values())
        configs = kwargs.get('configs', False)
        caches = kwargs.get('caches', False)
        plugins = kwargs.get('plugins', False)
        logs = kwargs.get('logs', False)

        if configs or everything:
            removed |= self.remove(CONFIGS, version)
        if caches or everything:
            removed |= self.remove(CACHES, version)
        if plugins or everything:
            removed |= self.remove(PLUGINS, version)
        if logs or everything:
            removed |= self.remove(LOGS, version)
        return removed

    @staticmethod
    def archive_project(project=PWD, target=DESKTOP, projects=PROJECTS):
        """Archive given project and send to target."""
        project, target, projects = str(project), str(target), str(projects)
        if os.sep not in project:
            project = os.path.join(projects, project)
        archive_path = os.path.join(target, project.split(os.sep)[-1])
        make_archive(base_name=archive_path, format='zip', root_dir=project)
        logging.info('Archive %s.zip is created', archive_path)

    @staticmethod
    def normalize_version(version):
        """Convert user given IDE version to standard format."""
        logging.debug('Normalize: version %s', version)
        match = re.match(r'(?P<ide>[a-zA-Z]+)(?P<version>[\d.]+)?', version)
        if not match or match.group('ide').lower() not in ALIASES:
            raise ValueError
        else:
            ide = ALIASES[match.group('ide').lower()]
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
    """Main application logic for Linux."""

    @staticmethod
    def remove(path, version):
        """Remove all version folders from path."""
        path = str(path).format(version=version)
        folders = glob(path)
        for folder in folders:
            logging.info('rm %s', folder)
            rmtree(folder)
        return bool(folders)

    def remove_all(self, version, **kwargs):
        """Remove given settings for given IDE version."""
        removed = False
        everything = not any(kwargs.values())
        if everything:
            removed |= self.remove(HOME + '/{version}', version)
        else:
            removed |= super(BanneretLinux, self).remove_all(version, **kwargs)
        return removed


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
