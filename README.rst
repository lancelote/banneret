.. image:: https://requires.io/github/lancelote/banneret/requirements.svg?branch=master
    :target: https://requires.io/github/lancelote/banneret/requirements/?branch=master

.. image:: https://travis-ci.org/lancelote/banneret.svg?branch=master
    :target: https://travis-ci.org/lancelote/banneret

.. image:: http://jb.gg/badges/team.svg
    :target: https://confluence.jetbrains.com/display/ALL/JetBrains+on+GitHub

banneret
========

PyCharm management swiss-army-knife.

Requirements
------------

- Python 2.7 or 3.6
- macOS

Supported
---------

- PyCharm
- IntelliJIdea

Usage
-----

Explore options with ``-h`` flag, some examples:

.. code::

    bnrt clean PyCharm2017.2   # to remove all PyCharm 2017.2 settings from system
    bnrt clean pycharm         # to remove all PyCharm versions settings
    bnrt clean idea            # to remove all IntelliJIdea versions settings
    bnrt clean PyCharmCE       # to remove all community editions settings

    bnrt archive               # to zip current folder and send it to desktop
    bnrt archive -p hello      # to zip project named "hello" in PycharmProjects
    bnrt archive -t /opt       # to zip current folder and send it to /opt

    bnrt docker                # to remove all containers, images and volumes
    bnrt docker -i             # to remove all docker images

    bnrt errors pycharm2017.2  # to enable exception notifications for PyCharm2017.2
    bnrt errors -d pycharm     # to disable exception notifications for all PyCharms

    bnrt -v <command>          # verbose output for debugging
    bnrt --version             # script version

Development
-----------

For repository tasks ``Makefile`` is used, try ``make help`` to view available commands.
