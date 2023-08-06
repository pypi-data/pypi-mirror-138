# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tracerepo']

package_data = \
{'': ['*']}

install_requires = \
['fractopo>=0.3.0,<0.4.0',
 'json5>=0.9.6,<0.10.0',
 'nialog>=0.0.1,<0.0.2',
 'pandas',
 'pandera',
 'pydantic>=1.8.2,<2.0.0',
 'pyproj>=3.1,<3.2',
 'rich',
 'typer']

extras_require = \
{'coverage': ['coverage>=5.0,<6.0', 'coverage-badge'],
 'docs': ['sphinx',
          'sphinx-rtd-theme',
          'nbsphinx',
          'sphinx-gallery',
          'sphinx-autodoc-typehints',
          'sphinx-autobuild'],
 'format-lint': ['sphinx',
                 'pylint',
                 'rstcheck',
                 'black[jupyter]',
                 'blacken-docs',
                 'blackdoc',
                 'isort'],
 'typecheck': ['mypy']}

entry_points = \
{'console_scripts': ['tracerepo = tracerepo.cli:app']}

setup_kwargs = {
    'name': 'tracerepo',
    'version': '0.0.7',
    'description': 'Fracture & lineament data management.',
    'long_description': 'Documentation\n=============\n\n|Documentation Status| |PyPI Status| |CI Test| |Coverage|\n\nRunning tests\n-------------\n\nTo run pytest in currently installed environment:\n\n.. code:: bash\n\n   poetry run pytest\n\nTo run full extensive test suite:\n\n.. code:: bash\n\n   poetry run doit\n   # Add -n <your-cpu-core-count> to execute tasks in parallel\n   # E.g.\n   poetry run doit -n 8 -v 0\n   # -v 0 is added to limit verbosity to mininum (optional)\n   # doit makes sure tasks are run in the correct order\n   # E.g. if a task uses a requirements.txt file that other task produces\n   # the producer is run first even with parallel execution\n\nFormatting and linting\n----------------------\n\n\nFormatting & linting:\n\n.. code:: bash\n\n   poetry run doit format\n   poetry run doit lint\n\nBuilding docs\n-------------\n\nDocs can be built locally to test that ``ReadTheDocs`` can also build them:\n\n.. code:: bash\n\n   poetry run doit docs\n\ndoit usage\n----------\n\nTo list all available commands from ``dodo.py``:\n\n.. code:: bash\n\n   poetry run doit list\n\nDevelopment\n~~~~~~~~~~~\n\nDevelopment dependencies for ``tracerepo`` include:\n\n-  ``poetry``\n\n   -  Used to handle Python package dependencies.\n\n   .. code:: bash\n\n      # Use poetry run to execute poetry installed cli tools such as invoke,\n      # nox and pytest.\n      poetry run <cmd>\n\n\n-  ``doit``\n\n   -  A general task executor that is a replacement for a ``Makefile``\n   -  Understands task dependencies and can run tasks in parallel\n      even while running them in the order determined from dependencies\n      between tasks. E.g. requirements.txt is a requirement for running\n      tests and therefore the task creating requirements.txt will always\n      run before the test task.\n\n   .. code:: bash\n\n      # Tasks are defined in dodo.py\n      # To list doit tasks from command line\n      poetry run doit list\n      # To run all tasks in parallel (recommended before pushing and/or\n      # committing)\n      # 8 is the number of cpu cores, change as wanted\n      # -v 0 sets verbosity to very low. (Errors will always still be printed.)\n      poetry run doit -n 8 -v 0\n\n-  ``nox``\n\n   -  ``nox`` is a replacement for ``tox``. Both are made to create\n      reproducible Python environments for testing, making docs locally, etc.\n\n   .. code:: bash\n\n      # To list available nox sessions\n      # Sessions are defined in noxfile.py\n      poetry run nox --list\n\n-  ``copier``\n\n   -  ``copier`` is a project templater. Many Python projects follow a similar\n      framework for testing, creating documentations and overall placement of\n      files and configuration. ``copier`` allows creating a template project\n      (e.g. https://github.com/nialov/nialov-py-template) which can be firstly\n      cloned as the framework for your own package and secondly to pull updates\n      from the template to your already started project.\n\n   .. code:: bash\n\n      # To pull copier update from github/nialov/nialov-py-template\n      poetry run copier update\n\n\n-  ``pytest``\n\n   -  ``pytest`` is a Python test runner. It is used to run defined tests to\n      check that the package executes as expected. The defined tests in\n      ``./tests`` contain many regression tests (done with\n      ``pytest-regressions``) that make it almost impossible\n      to add features to ``tracerepo`` that changes the results of functions\n      and methods.\n\n   .. code:: bash\n\n      # To run tests implemented in ./tests directory and as doctests\n      # within project itself:\n      poetry run pytest\n\n\n-  ``coverage``\n\n   .. code:: bash\n\n      # To check coverage of tests\n      # (Implemented as nox session!)\n      poetry run nox --session test_pip\n\n-  ``sphinx``\n\n   -  Creates documentation from files in ``./docs_src``.\n\n   .. code:: bash\n\n      # To create documentation\n      # (Implemented as nox session!)\n      poetry run nox --session docs\n\nBig thanks to all maintainers of the above packages!\n\nLicense\n~~~~~~~\n\nCopyright © 2021, Nikolas Ovaskainen.\n\n-----\n\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/tracerepo/badge/?version=latest\n   :target: https://tracerepo.readthedocs.io/en/latest/?badge=latest\n.. |PyPI Status| image:: https://img.shields.io/pypi/v/tracerepo.svg\n   :target: https://pypi.python.org/pypi/tracerepo\n.. |CI Test| image:: https://github.com/nialov/tracerepo/workflows/test-and-publish/badge.svg\n   :target: https://github.com/nialov/tracerepo/actions/workflows/test-and-publish.yaml?query=branch%3Amaster\n.. |Coverage| image:: https://raw.githubusercontent.com/nialov/tracerepo/master/docs_src/imgs/coverage.svg\n   :target: https://github.com/nialov/tracerepo/blob/master/docs_src/imgs/coverage.svg\n',
    'author': 'nialov',
    'author_email': 'nikolasovaskainen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nialov/tracerepo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
