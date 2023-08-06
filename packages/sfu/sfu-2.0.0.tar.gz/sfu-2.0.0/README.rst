===
sfu
===

Snowflake URI utility library that supports extraction of Snowflake configuration data and method parameters from Snowflake resource URIs.

|pypi| |readthedocs| |actions|

.. |pypi| image:: https://badge.fury.io/py/sfu.svg
   :target: https://badge.fury.io/py/sfu
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/sfu/badge/?version=latest
   :target: https://sfu.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/nthparty/sfu/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/nthparty/sfu/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/nthparty/sfu/badge.svg?branch=main
   :target: https://coveralls.io/github/nthparty/sfu?branch=main
   :alt: Coveralls test coverage summary.

Purpose
-------
When applications that employ the `Snowflake Python SDK <https://docs.snowflake.com/en/user-guide/python-connector.html>`_ must work with resources that are spread across multiple accounts, it can be useful to tie Snowflake configuration information (both credentials and resource data) directly tot associated Snowflake resources (*e.g.*, by including the  configuration data within URIs). This library provides a class that extracts Snowflake configuration data and method  parameters from a URI, offering a succint syntax for passing (directly into Snowflake methods) configuration data and/or resource names that are included within URIs.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install sfu

The sfu class can be imported with::

    from sfu import sfu

The class provides methods for extracting configuration data (credentials and non-credentials) from URIs, as in the examples below::

    >>> from sfu import sfu
    >>> import snowflake.connector

    # Create a connector client given a URI (for a table in some snowflake database) that
    # includes credentials (a username 'ABC', a password 'XYZ', and an associated account
    # 'UVW').
    # Make sure the account contains the region and platform, e.g., xxx.us-east-1.aws.
    >>> s = sfu("snow://ABC:XYZ:UVW@DATABASE")
    >>> conn = connector.connect(**s.credentials())

    # It can also be useful to bind a connection to some database and some data processing
    # warehouse, so you don't need to execute cursor commands later. The following will
    # return a connector client that is configured against DATABASE, using WH for data
    # processing.
    >>> uri = "snow://ABC:XYZ:UVW@DATABASE/TABLE@warehouse=WH"
    >>> s = sfu(uri)
    >>> c = connector.connect(**s.for_connection())
    >>> cs = c.cursor()
    >>> cs.execute(f"SELECT col1,col2 FROM {s.for_table()}")

    # Note that this is equivalent to the following:
    >>> s = sfu(uri)
    >>> c = connector.connect(**s.credentials())
    >>> cs = c.cursor()
    >>> cs.execute(f"USE DATABASE {s.for_db()}")
    >>> cs.execute(f"USE WAREHOUSE {s.for_warehouse()}")
    >>> cs.execute(f"SELECT col1,col2 FROM {s.for_table()}")

Developer Notes
---------------

Pipenv is used for dependency management of the main library, minus Read the Docs which does not support Pipenv.
You can install all dependencies with::

    pipenv install --dev

To release a new version of the library, run::

    pipenv run python -m pip install --upgrade build twine
    pipenv run python -m build
    pipenv run python -m twine upload dist/*

Documentation
-------------

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    python -m pip install -e .
    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `pytest <https://pytest.org>`_::

  pipenv run python -m pytest --cov=sfu --cov-report term-missing

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

  pipenv run python -m flake8 src/sfu

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
