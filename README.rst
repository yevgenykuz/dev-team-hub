Dev Team Hub - A basic website for development teams
####################################################

The site is meant to bridge between a development team that develops internal products for its company,
and the users of those products.

The site contains 3 basic sections - news, wiki and forum. Read more about them below.


.. image:: https://user-images.githubusercontent.com/19968607/38177374-fbe48382-3608-11e8-9fb3-64a46982b953.gif


.. image:: https://travis-ci.org/yevgenykuz/dev-team-hub.svg?branch=master
    :target: https://travis-ci.org/yevgenykuz/dev-team-hub
.. image:: https://coveralls.io/repos/github/yevgenykuz/dev-team-hub/badge.svg?branch=master
    :target: https://coveralls.io/github/yevgenykuz/dev-team-hub?branch=master
.. image:: https://gemnasium.com/badges/github.com/yevgenykuz/dev-team-hub.svg
    :target: https://gemnasium.com/github.com/yevgenykuz/dev-team-hub



.. contents:: :local:

Features
========
* **News section** - contains announcements from the development team (release notes, infrastructure maintenance and changes, important updates, etc.). Articles are filtered by tags
* **Wiki section** - the knowledge base of the development team and its products (product information, infrastructure information, development guidelines, etc.). Entries can share common "custom fields" to reduce copy-paste clutter
* **Forum section** - a public place to discuss and ask questions (support, product suggestions, development flow suggestions, etc.)
* **Account page** - contains "favorite wiki entries" and "posts opened by me"
* **Basic search** - performs full text search on wiki entries, news articles, and forum topics
* **On the fly site configuration** - site name, custom links drop-down, and current product version can be changed without accessing source files

Prerequisites
=============
* Python 3.6
* PostgreSQL DB for full text search
* Everything in `requirements.txt <https://github.com/yevgenykuz/dev-team-hub/blob/master/requirements.txt>`_

Deployment (as a development server)
====================================
On Ubuntu, follow the following steps (other OS - same process, different commands):

Install PostgreSQL DB
---------------------

Get it:

.. code-block:: bash

    sudo apt-get -y install postgresql postgresql-contrib
    
Set it up:

.. code-block:: bash

    sudo su - postgres
    createuser u_devteamhub
    createdb devteamhub --owner u_devteamhub
    psql -c "ALTER USER u_devteamhub WITH PASSWORD 'YOURSUPERSECRETPASSWORD'"
    exit

Clone the source code
---------------------

In your working folder (your home folder, for example)

.. code-block:: bash

    git clone https://github.com/yevgenykuz/dev-team-hub.git 

Configure your project
----------------------

This project uses python-decouple and dj-database-url to organize django settings.
Therefore, you need to create a local .env file and edit it before running the server.
Use the provided .travis.env file as reference.
For basic usage, you must have the following settings:

.. code-block:: bash

    # in your .env file
    DEBUG=True
    SECRET_KEY=YOURSUPERSECRETKEY
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=postgres://u_devteamhub:YOURSUPERSECRETPASSWORD@localhost:5432/devteamhub
    LOG_LEVEL=INFO

Run it as a Django server
-------------------------

Make sure you have all python dependencies installed (i recommend using a `virutalenv <https://virtualenv.pypa.io/en/stable/>`_):

.. code-block:: bash

    # inside the folder you've just cloned:
    pip install -r requirements.txt

Now run it as a Django development server:

.. code-block:: bash

    # inside the folder you've just cloned:
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Authors
=======
`yevegnykuz <https://github.com/yevegnykuz>`_

License
=======
BSD-3-Clause - `LICENSE <https://github.com/yevgenykuz/dev-team-hub/blob/master/LICENSE>`_

-----
