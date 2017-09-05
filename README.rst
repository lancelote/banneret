.. image:: https://requires.io/github/lancelote/banneret/requirements.svg?branch=master
    :target: https://requires.io/github/lancelote/banneret/requirements/?branch=master

.. image:: https://travis-ci.org/lancelote/banneret.svg?branch=master
    :target: https://travis-ci.org/lancelote/banneret

banneret
========

PyCharm management swiss-army-knife

requirements
------------

- Python 3.6
- macOS

supported
---------

- PyCharm
- IntelliJIdea

usage
-----

.. code::

    bnrt clean PyCharm2017.2  # to remove all PyCharm 2017.2 settings from system
    bnrt clean pycharm        # to remove all PyCharm versions settings
    bnrt clean idea           # to remove all IntelliJIdea versions settings
    bnrt clean PyCharmCE      # to remove all community editions settings

    bnrt archive              # to zip current folder and send it to desktop
    bnrt archive -p hello     # to zip project named "hello" in PycharmProjects
    bnrt archive -t /opt      # to zip current folder and send it to /opt

    bnrt -v <command>         # verbose output for debugging

management
----------

for repository tasks ``Makefile`` is used, try ``make help`` to view available commands
