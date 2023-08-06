# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['package_1', 'package_2']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['furo',
          'myst-parser',
          'pdoc3',
          'pydata-sphinx-theme',
          'python-docs-theme',
          'sphinx',
          'sphinx-book-theme',
          'sphinx-theme-pd',
          'sphinx_rtd_theme<=2.0.0',
          'sphinxcontrib-mermaid']}

entry_points = \
{'console_scripts': ['add-1-2 = package_1.__main__:main',
                     'sample-command = package_2.__main__:main'],
 'pseudo_package.plugin': ['sample-plugin = package_1.plugins:plugin_call']}

setup_kwargs = {
    'name': 'python-project-templates',
    'version': '0.1.1',
    'description': '',
    'long_description': "# Python Project Template\n\nThis is a template repository for python project.\n\ncheck [GitHub document](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) aboud template repository.\n\n\n## CI/CD badges.\n[![Python package](https://github.com/kagemeka/python-project-template/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/python-project-template/actions/workflows/python-package.yml)\n[![readthedocs build status](https://readthedocs.org/projects/python-project-templates/badge/?version=latest)](https://python-project-templates.readthedocs.io/en/latest/?badge=latest)\n\nfor detail, see\n- [GitHub documentation](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge)\n- [readthedocs build badges](https://docs.readthedocs.io/en/stable/badges.html)\n\n## docker environment\nUse docker environment to avoid annoying conflicts. \\\nFirst, you must set the project name in `docker/.env` file. \\\nthen you can run `docker-compose up -d` command\nto build an docker image with default Dockerfile.\n```bash\n$ cd docker \\\n    && docker-compose up -d\n```\nfor details about docker, see official documentations\n- [Docker](https://docs.docker.com/)\n- [Docker Compose](https://docs.docker.com/compose/)\n\n\n\n## Documenting\nYou can use documenting tools like\n- [sphinx](https://www.sphinx-doc.org/en/master/)\n- [mkdocs](https://www.mkdocs.org/)\n\nand host it on [readthedocs](https://docs.readthedocs.io/)\n\n[`Python Project Template`'s documentation](https://python-project-templates.readthedocs.io/)\n---\n\n### sphinx\n#### [shpinx-apidoc](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)\ngenerate document with sphinx-apidoc command.\n[script](scripts/generate_sphinx_docs.sh)\n\n\n#### configurations (todo)\nsphinx extensions\nhttps://www.sphinx-doc.org/en/master/usage/extensions/index.html\n\nnapoleon\nhttps://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon\n\nnumpy style\nhttps://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard\n\ngoogle style\nhttps://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings\n\n\n## publish package to Pypi\n[![PyPI version](https://badge.fury.io/py/python-project-templates.svg)](https://badge.fury.io/py/python-project-templates)\n\n[the page of this project](https://pypi.org/project/python-project-templates/)\n\n\n## license\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n",
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
