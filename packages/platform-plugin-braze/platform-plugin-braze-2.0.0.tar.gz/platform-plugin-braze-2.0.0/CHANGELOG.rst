Change Log
----------

..
   All enhancements and patches to edx_braze will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

*

[2.0.0] - 2022-02-16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Dropped support for Django22, 30 and 31
* Added Django40 support

[1.2.0] - 2021-12-14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Support added for identifying alias-only ``save_for_later`` users in Braze,
  when a user with a matching email registers in the LMS

[1.1.0] - 2021-09-21
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added support for Django 3.1 and 3.2

[1.0.0] - 2021-06-04
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* First release
* Supports identifying alias-only ``hubspot`` users in Braze, when a user
  with a matching email registers in the LMS.
