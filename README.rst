Dev Team Hub - A basic website for development teams
####################################################

The site is meant to bridge between a development team that develops internal products for its company,
and the users of those products.

The site contains 3 basic sections - news, wiki and forum. Read more about them below.


.. class:: no-web

    .. image:: https://user-images.githubusercontent.com/19968607/38177374-fbe48382-3608-11e8-9fb3-64a46982b953.gif
        :alt: Dev Team Hub demo
        :width: 100%
        :align: center


.. class:: no-web no-pdf

|travis_ci| |coverage|

-----


.. contents::

.. section-numbering::



Features
========

* **News section** - contains announcements from the development team (release notes, infrastructure maintenance and
  changes, important updates, etc.). Articles are filtered by tags
* **Wiki section** - the knowledge base of the development team and its products (product information, infrastructure
  information, development guidelines, etc.). Entries can share common "custom fields" to reduce copy-paste clutter
* **Forum section** - a public place to discuss and ask questions (support, product suggestions, development flow
  suggestions, etc.)
* **Account page** - contains "favorite wiki entries" and "posts opened by me"
* **Basic search** - performs full text search on wiki entries, news articles, and forum topics
* **On the fly site configuration** - site name, custom links drop-down, and current product version can be changed
  without accessing source files

Deployment (as a development server)
====================================

This project requires:

* Python 3.6
* PostgreSQL DB for full text search
* Everything in `requirements.txt <https://github.com/yevgenykuz/dev-team-hub/blob/master/requirements.txt>`_


On Ubuntu, follow the following steps (other OS - same process, different commands):

Install PostgresSQL DB
----------------------

Get it:

.. code-block:: bash

    # linux:
    sudo apt-get -y install postgresql postgresql-contrib python-psycopg2 libpq-dev
    # mac with brew:
    brew install postgresql
    brew services run postgresql
    # You can also run "brew services start postgresql" to have it start at boot
    # or run "/usr/local/opt/postgresql@14/bin/postgres -D /usr/local/var/postgres"
    # to see the DB logs in terminal

    
Set it up:

.. code-block:: bash

    # linux:
    sudo su - postgres
    # create a db user and password and allow DB creation for django test suite
    createuser u_devteamhub
    psql -c "ALTER USER u_devteamhub WITH PASSWORD 'YOURSUPERSECRETPASSWORD'"
    psql -c "ALTER USER u_devteamhub CREATEDB"
    # create db for local server
    createdb devteamhub --owner u_devteamhub
    exit

    # macos, if you installed postgresql with brew and using psql:
    psql postgres
    # create a db user and password and allow DB creation for django test suite
    CREATE ROLE u_devteamhub WITH LOGIN PASSWORD 'YOURSUPERSECRETPASSWORD';
    ALTER ROLE u_devteamhub CREATEDB;
    # create db for local server
    CREATE DATABASE devteamhub WITH OWNER 'u_devteamhub';
    \q

Clone the source code
---------------------

In your working folder (your home folder, for example)

.. code-block:: bash

    git clone https://github.com/yevgenykuz/dev-team-hub.git 

Configure your project
----------------------

| This project uses `python-decouple <https://pypi.python.org/pypi/python-decouple>`_ and
  `dj-database-url <https://pypi.python.org/pypi/dj-database-url>`_ to organize django settings.
| You need to create a local .env file and edit it before running the server.
| Use the provided .travis.env file as reference.
| For basic usage, you must have the following settings (using the db username and password from
  `Install PostgreSQL DB`_):

.. code-block:: bash

    # in your .env file
    DEBUG=True
    SECRET_KEY=YOURSUPERSECRETKEY
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=postgres://u_devteamhub:YOURSUPERSECRETPASSWORD@localhost:5432/devteamhub
    LOG_LEVEL=INFO

Run it as a Django server
-------------------------

Make sure you have all python dependencies installed (i recommend using
`virutalenv <https://pypi.python.org/pypi/virtualenv>`_):

.. code-block:: bash

    # inside the folder you've just cloned:
    pip install -r requirements.txt

Now run it as a Django development server:

.. code-block:: bash

    # inside the folder you've just cloned:
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Meta
====

Authors
-------

`yevgenykuz <https://github.com/yevgenykuz>`_

License
-------

`MIT License <https://github.com/yevgenykuz/dev-team-hub/blob/master/LICENSE>`_

-----


.. |travis_ci| image:: https://travis-ci.org/yevgenykuz/dev-team-hub.svg?branch=master
    :target: https://travis-ci.org/yevgenykuz/dev-team-hub
    :alt: Travis CI

.. |coverage| image:: https://coveralls.io/repos/github/yevgenykuz/dev-team-hub/badge.svg?branch=master
    :target: https://coveralls.io/github/yevgenykuz/dev-team-hub?branch=master
    :alt: Test coverage
