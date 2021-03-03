User Guide
==========


Usage as Python library
-----------------------

This project is usable as a Python library.

Install the latest version of the project from PyPI:

.. code-block::

  pip install -U cdn-definitions

CDN definitions may then be accessed via a few methods in
the ``cdn_definitions`` module, as in example:

.. code-block:: python

   from cdn_definitions import load_data

   DATA = load_data(source="https://raw.githubusercontent.com/release-engineering/cdn-definitions/master/src/cdn_definitions/data.json")
   for alias in DATA["rhui_alias"]:
     if my_path.startswith(alias["src"]):
       # my path falls under a /rhui/ alias,
       # so now do something special

If a source is not specified, the library will use data from the first existing of the following
sources:

- A JSON or YAML file pointed at by the ``CDN_DEFINITIONS_PATH`` environment variable.
- The file bundled with the library on PyPI.
- ``/usr/share/cdn-definitions/data.yaml``.

Note that loading from the release-engineering/cdn-definitions repo as seen above will yield
placeholder/reference data. This reference data aims to give a general idea of the data's
structure and purpose, and also enable automated testing within downstream projects consuming
cdn-definitions.

However, in production scenarios it will be necessary to deploy your code pointing at a genuine
data set. This will typically be accomplished either by calling ``load_data`` passing the URL of
an internal data set, or ensuring that ``CDN_DEFINITIONS_PATH`` is set appropriately where your
code is deployed.


Python reference
.............

.. module:: cdn_definitions

.. autofunction:: load_data

.. autofunction:: load_schema
