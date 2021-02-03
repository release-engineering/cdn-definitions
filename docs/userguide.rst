User Guide
==========


Usage as online dataset
-----------------------

The latest version of this dataset can be downloaded at any time from URLs:

- https://release-engineering.github.io/cdn-definitions/data.json
- https://release-engineering.github.io/cdn-definitions/data.yaml

Both files contain equivalent data.




Usage as packaged dataset
-------------------------

This dataset is available as an RPM from selected Red Hat internal repositories.

- Enable ``eng-rhel-6``, ``eng-rhel-7`` or equivalent yum repository on the target system.
- Install the ``cdn-definitions`` package. This package has no dependencies.
- Load data from ``/usr/share/cdn-definitions/data.json``
  or ``/usr/share/cdn-definitions/data.yaml``.


Usage as Python library
-----------------------

This project is usable as a Python library.

Install the latest version of the project from PyPI:

.. code-block::

  pip install -U cdn-definitions

CDN definitions may then be accessed via a few methods in
the ``cdn_definitions`` module, as in example:

.. code-block:: python

  from cdn_definitions import rhui_aliases

  for alias in rhui_aliases():
    if my_path.startswith(alias.src):
      # my path falls under a /rhui/ alias,
      # so now do something special

The library will use data from the first existing of the following sources:

- A JSON or YAML file pointed at by the ``CDN_DEFINITIONS_PATH`` environment variable.
- The file bundled with the library on PyPI.
- ``/usr/share/cdn-definitions/data.yaml``.

To ensure the most up-to-date definitions, upgrade the package from PyPI.


Python reference
.............

.. module:: cdn_definitions

.. autoclass:: PathAlias()
   :members:

.. autofunction:: rhui_aliases

.. autofunction:: origin_aliases
