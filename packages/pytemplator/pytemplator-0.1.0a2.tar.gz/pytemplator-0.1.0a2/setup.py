# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytemplator']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'PyYAML>=6.0,<7.0', 'loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['pytemplate = pytemplator.cli:main']}

setup_kwargs = {
    'name': 'pytemplator',
    'version': '0.1.0a2',
    'description': 'Pytemplator aims to streamline the creation of dynamic templates. It is inspired from the excellent CookieCutter package but offers more flexibility.',
    'long_description': '===========\nPytemplator\n===========\n\n\n.. image:: https://img.shields.io/pypi/v/pytemplator.svg\n        :target: https://pypi.python.org/pypi/pytemplator\n\n\n.. image:: https://pyup.io/repos/github/arnaudblois/pytemplator/shield.svg\n     :target: https://pyup.io/repos/github/arnaudblois/pytemplator/\n     :alt: Updates\n\n\n\nPytemplator aims to streamline the creation of dynamic templates.\nIt supports the format from `CookieCutter package`_ but also offers the option\nto generate the context using Python, which in practice provides a better user\nexperience and more flexibility.\n\n\n* Free software: Apache Software License 2.0\n* Documentation: https://arnaudblois.github.io/pytemplator/.\n\nHow to use\n----------\n\n- Install the package `pytemplator` using pip or poetry.\n- In a shell::\n\n  $ pytemplate <target>\n\nWhere `<target>` can be either a local path to the directory of a Pytemplator template\nor the url to a git repo.\n\nThere are options to specify which branch should be used for templating,\nthe output directory and the config directory. More details can be obtained with::\n\n  $ pytemplate --help\n\n\n\nFor template developers\n-----------------------\n\nExample\n~~~~~~~\n\nSee this `project example`_ to get an idea of an actual pytemplator template.\n\n.. _`project example`: https://github.com/arnaudblois/pypi-package-template\n\nGeneral idea\n~~~~~~~~~~~~\n\nA typical Pytemplator template project can live either as a local directory or as a Git repo.\nIt relies on three elements:\n- a `templates` folder where all folders and files to be templated should be placed.\nUnder the hood, pytemplator relies on jinja2.\n- an `initialize.py` at the root level with a function "generate_context". More details below.\n- a `finalize.py` whose `finalize` function is run after the templating.\n\n\nThe `generate_context` function\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nThe `generate_context` function should return a dictionary mapping the variables in the\ntemplate to their values. The idea is to use the extra flexibility to offer sensible default\nvalues to make the user experience smoother.\n\n`generate_context` must accept `no_input` as argument. This tells what should happen in purely\nprogrammatic environment. It is up to you how you\'d like to address this, you can provide default values\nif this makes sense and choose not to handle it, in which case a NoInputOptionNotHandledByTemplateError\nwill be raised.\n\nThere are several utility classes to help, `Context` and `Question`.\n\nThe following code illustrates how they can be used::\n\n  import datetime\n\n  from pytemplator.utils import Question as Q, Context\n\n  def generate_context(no_input, *args, **kwargs):\n      """Generate context."""\n\n      context = Context()\n\n      context.questions = [\n          Q("pypi_name", ask="Name of the package on Pypi"),\n          Q("module_name", ask=False, default=lambda: context["pypi_name"].replace("-","_").lower()),\n          Q("year", default=date.today().year, ask=False),\n      ]\n      context.resolve(no_input)\n      return context.as_dict()\n\nA `Question` takes several arguments:\n- the key that will be put in the context, required.\n- `ask` is the prompt displayed to the user, a default inferred from the key is\ndisplayed if this is left to None. Set this to False to take the default without\nasking the user.\n- `default` is the value by default. This can be either a value or a callable.\nThe latter allows for lazy evaluation, especially useful to look into the context\nto use answers from previous questions.\n- `no_input_default` is the value used when `no_input` is True. If None, `default`\nis used.\n\n\nContributing\n------------\n\nAll help is much appreciated and credit is always given.\nPlease consult CONTRIBUTING.rst for details on how to assist me.\n\n\nCredits\n-------\n\nThis package is inspired from the excellent `CookieCutter package`_ and `audreyr/cookiecutter-pypackage`_ project template.\n\n\n.. _`CookieCutter package`: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Arnaud Blois',
    'author_email': 'hi@arnaudblois.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
