import os
from distutils.core import setup

from setuptools import find_packages

__version__ = 'unknown'
version_path = os.path.join(os.path.split(__file__)[0], 'banneret/version.py')

with open(version_path) as version_file:
    exec(version_file.read())

URL = 'https://github.com/lancelote/banneret'

setup(
    name='banneret',
    packages=find_packages(exclude=['tests', '*.test', '*.test.*']),
    version=__version__,
    description='CLI helpers for PyCharm management',
    author='Pavel Karateev',
    author_email='pavel.karateev@jetbrains.com',
    url=URL,
    download_url=URL + '/archive/{}.tar.gz'.format(__version__),
    keywords=['pycharm', 'cli'],
    entry_points={
        'console_scripts': [
            'bnrt = banneret.main:main'
        ]
    },
    install_requires=[],
    extras_require={
        'test': ['pytest', 'pytest-mock', 'tox'],
        'docker': ['docker']
    }
)
