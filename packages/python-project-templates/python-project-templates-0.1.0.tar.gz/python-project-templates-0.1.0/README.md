# Python Project Template

## CI/CD badges.
[![Python package](https://github.com/kagemeka/python-project-template/actions/workflows/python-package.yml/badge.svg)](https://github.com/kagemeka/python-project-template/actions/workflows/python-package.yml)
[![readthedocs build status](https://readthedocs.org/projects/python-project-templates/badge/?version=latest)](https://python-project-templates.readthedocs.io/en/latest/?badge=latest)

for detail, see
- [GitHub documentation](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge)
- [readthedocs build badges](https://docs.readthedocs.io/en/stable/badges.html)

## docker environment
Use docker environment to avoid annoying conflicts.
First, you must set the project name in `docker/.env` file.
then you can run `docker-compose up -d` command
to build an docker image with default Dockerfile.
```bash
$ cd docker \
    && docker-compose up -d
```
for details about docker, see official documentations
- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)



## Documenting
You can use documenting tools like
- [sphinx](https://www.sphinx-doc.org/en/master/)
- [mkdocs](https://www.mkdocs.org/)

and host it on [readthedocs](https://docs.readthedocs.io/)

[`Python Project Template`'s documentation](https://python-project-templates.readthedocs.io/)
---

### sphinx
#### shpinx-apidoc
https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
generate document with sphinx-apidoc command.
```bash
$ sphinx
```


sphinx extensions
https://www.sphinx-doc.org/en/master/usage/extensions/index.html


napoleon
https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon

numpy style
https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard

google style
https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
