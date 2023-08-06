platform-plugin-braze
=====================

|ci-badge| |codecov-badge|

This is an edx-platform plugin designed to integrate with edx.org's Braze
account.

One major thing it does is ``identify`` hubspot-alias-only accounts once a
user registers for an LMS account (thus merging the two Braze profiles into
one).

It's unique to edx.org's specific deployment and services, and thus is not
part of Open edX releases.

Overview
--------

This repo holds a single ``edx_braze`` djangoapp module, meant to be
pip-installed during deployment of ``edx-platform`` and which will register
itself as an `edx platform plugin`_.

.. _edx platform plugin: https://github.com/edx/edx-django-utils/tree/master/edx_django_utils/plugins

Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block::

  # Clone the repository
  git clone git@github.com:edx/platform-plugin-braze.git
  cd platform-plugin-braze

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 platform-plugin-braze


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

  # Activate the virtualenv
  workon platform-plugin-braze

  # Grab the latest code
  git checkout master
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

.. |ci-badge| image:: https://github.com/edx/platform-plugin-braze/workflows/Python%20CI/badge.svg?branch=master
    :target: https://github.com/edx/platform-plugin-braze/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/edx/platform-plugin-braze/coverage.svg?branch=master
    :target: https://codecov.io/github/edx/platform-plugin-braze?branch=master
    :alt: Codecov
