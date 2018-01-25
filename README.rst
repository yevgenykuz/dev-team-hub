**Dev Team Hub**

.. image:: https://travis-ci.org/yevgenykuz/dev-team-hub.svg?branch=master
    :target: https://travis-ci.org/yevgenykuz/dev-team-hub
.. image:: https://coveralls.io/repos/github/yevgenykuz/dev-team-hub/badge.svg?branch=master
    :target: https://coveralls.io/github/yevgenykuz/dev-team-hub?branch=master
.. image:: https://gemnasium.com/badges/github.com/yevgenykuz/dev-team-hub.svg
    :target: https://gemnasium.com/github.com/yevgenykuz/dev-team-hub

-----

A basic website for development teams.
The site is meant to bridge between a development team that develops internal products for its company,
and the users of those products.
The site contains 3 basic sections - news, wiki and forum. Read more about them below.

-----

.. contents:: :local:

Features
========
* News section - contains announcements from the development team (release notes, infrastructure maintenance and changes, important updates, etc.). Articles are filtered by tags
* Wiki section - the knowledge base of the development team and its products (product information, infrastructure information, development guidelines, etc.). Entries can share common "custom fields" to reduce copy-paste clutter
* Forum section - a public place to discuss and ask questions (support, product suggestions, development flow suggestions, etc.)
* Account page - contains "favorite wiki entries" and "posts opened by me"
* Basic search - performs full text search on wiki entries, news articles, and forum topics
* On the fly site configuration - site name, custom links drop-down, and current product version can be changed without accessing source files

Prerequisites
=============
* Python 3.6
* PostgreSQL DB for full text search
* Everything in `requirements.txt <https://github.com/yevgenykuz/dev-team-hub/blob/master/requirements.txt>`_

Deployment
==========
* Standard Django site deployment

Authors
=======
* `yevegnykuz <https://github.com/yevegnykuz>`_

License
=======
BSD-3-Clause - `LICENSE <https://github.com/yevgenykuz/dev-team-hub/blob/master/LICENSE>`_

-----

**Project is under development, may be unstable**
