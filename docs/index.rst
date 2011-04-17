
======================
webunit2 Documentation
======================

``webunit2`` is a spiritual successor to `Richard Jones' webunit
<http://mechanicalcat.net/tech/webunit/>`_, but is by no means a fork.  This
library has been built from the ground up, complete with documentation and
testing.  It's also `hosted on GitHub <https://github.com/amcfague/webunit2>`_,
making it a cinch to fork.

Why?
----

I developed the need for ``webunit`` when I decided to standardize a lot of the
testing for the company I work for.  Since many of the applications managed by
our team were backend services, having an easy way of wrapping web calls was a
must, and that's where I stumbled upon the original ``webunit``.

However, I found that many things were missing--documentation was sparse, header
manipulation wasn't available in the library, and the repository housing the
sources was nowhere to be found.  Additionally, it only supported a subset of
the HTML protocols, due to the :class:`httplib` backend.  This was fine for much
of the frontend usage that ``webunit`` was designed for, but not so much for the
backend services I was trying to test.

Thus, ``webunit2`` was born one rainy Saturday.  In its current form, it's not
quite up to par with ``webunit2``, although it does support the features I
immediately needed.  Notably missing is cookie support, caching, web resource
fetching (CSS, images, etc.), and DOM parsing.

Overview
--------

To **run unittests**::

    # Standard faire
    $ nosetests

    # With coverage reports
    $ nosetests --with-coverage --cover-package=webunit2

To **build this documentation**::

    $ easy_install sphinx
    [...]
    $ python setup.py build_sphinx

The built documentation is available (by default) in :file:`build/sphinx/html`,
and can be viewed locally on your web browser without the need for a separate
web server.

Narrative Documentation
=======================

.. toctree::
    :maxdepth: 1
    :glob:

    narr/*

Reference Material
==================

.. toctree::
   :maxdepth: 2
   :glob:

   api/*

Index and Glossary
==================

* :ref:`genindex`
* :ref:`search`
