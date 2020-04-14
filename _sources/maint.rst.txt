Maintenance Guide
=================

This document is intended for software engineers and release engineers responsible
for making updates to this project.


Is your data appropriate for this project?
------------------------------------------

The content delivery toolchain is driven by many pieces of metadata and it is not
necessarily clear which pieces of metadata shall be maintained as a part of this
project.

Consider these rules of thumb when deciding whether certain metadata fits here:

  **Small dataset**
    If your dataset consists of less than a hundred or so items, it may be
    appropriate for this project. If it consists of thousands of items, it
    is definitely not appropriate.

  **Infrequent updates**
    If you expect you'll need to add/change pieces of data more often than at
    each new RHEL minor release (i.e. more than a few times per year), this
    is likely not the correct place to store your data.

  **No synchronized releases**
    If your data will have requirements similar to "This change to data must be
    released in environment A on date X and no earlier, then environment B on date Y
    and no earlier...", this project is likely inappropriate.

  **No secrets**
    If you anticipate that your dataset may sometimes contain information not to be
    published externally from Red Hat (for example, names of unannounced products),
    your data can't be added to this project.

  **Additions only**
    Most data hosted by this project is expected to be *added to*, and rarely if ever
    *changed* or *removed*.


Requirement: minimal dependencies
---------------------------------

For maximum portability, it is a requirement of this project that it is usable
with Python as old as version 2.6 and as new as the most recent Python 3.x at
any given point, with no dependencies on any additional Python modules beyond
those in the standard library.

This requirement only applies to the project's package as distributed to PyPI.
It's OK to add dependencies for the test suite or development scripts.


JSON vs YAML
------------

This project publishes both JSON and YAML datasets.  Both datasets contain the same
data, merely in a different format.

The motivations for publishing the data in both formats include:

- It's desired for the data to be somewhat human-readable and to include meaningful comments;
  this is possible with YAML but not JSON.
- It's desired for the data to be loadable from Python with no added dependencies; this is
  possible with JSON but not YAML.

Hence, the project treats YAML as the authoritative data source and provides equivalent
JSON files as a convenience to downstream projects.

When making changes to the project, only the YAML files should be modified directly.
JSON files can be rebuilt using the ``make-json`` script.  It is recommended to use
a pre-commit hook for this; see the next section.

If you make an update to YAML files but forget to rebuild the JSON files, the project's CI
system will detect this and reject your change.


Installing pre-commit hooks
---------------------------

When working on this project, it's recommended to enable the project's pre-commit hooks.
These hooks cover:

- ensuring any Python changes are formatted using the ``black`` autoformatter
- ensuring JSON files are kept up-to-date with any YAML changes

To prepare the hooks, run these commands (or equivalent):

.. code-block::

  pip install pre-commit
  pre-commit install

For more information about the pre-commit tool, see https://pre-commit.com/.


Downstream projects
-------------------

Some known or expected uses of this dataset from downstream projects are listed here.
Be aware that changes to the dataset may require updates to packages for these projects.

  **exodus-lambda**
    - Uses RHUI and origin aliases when resolving requests to the CDN.

  **engproduct-cli**
    - Enforces that all defined "from RHUI" content sets use paths matching
      RHUI aliases.

  **cdn-utils**
    - Uses defined RHUI aliases to decide whether or not a given RHSM Pulp
      repo is published via a RHUI alias; this influences configuration for
      the repo.

  **manifest-api**
    - Inherits a dependency on this dataset via ``cdn-utils``.
