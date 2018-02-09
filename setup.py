from distutils.core import setup

from setuptools import find_packages

from banneret import __version__

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
            'bnrt = banneret:main'
        ]
    },
    install_requires=['docker'],
)
