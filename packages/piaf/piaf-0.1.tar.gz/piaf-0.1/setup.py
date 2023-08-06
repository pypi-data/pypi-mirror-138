# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['piaf',
 'piaf.comm',
 'piaf.comm.mtp',
 'piaf.examples',
 'piaf.examples.two_platforms']

package_data = \
{'': ['*']}

extras_require = \
{'amqp-mtp': ['aiormq>=6,<7', 'yarl>=1,<2']}

setup_kwargs = {
    'name': 'piaf',
    'version': '0.1',
    'description': 'A FIPA-compliant Agent Platform written in python.',
    'long_description': '# Python Intelligent Agent Framework (piaf)\n\n![pipeline status](https://gitlab.com/ornythorinque/piaf/badges/master/pipeline.svg)\n![coverage report](https://gitlab.com/ornythorinque/piaf/badges/master/coverage.svg?job=test)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/piaf)\n![PyPI - License](https://img.shields.io/pypi/l/piaf)\n![PyPI](https://img.shields.io/pypi/v/piaf)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/piaf)\n\nThe aim of piaf is to provide a FIPA-compliant agent framework using Python. It uses **asyncio** to power agents.\n\n## Project status\n\n**The first official release is there!** After almost two years of development, I am now considering piaf is stable enough to start playing with it. I can\'t wait to see the amazing things you will do!\n\nSo, what is next ? Well there are still missing features in piaf and the next version will try to add some of them (I see you FIPA SL!).\n\n## Features\n\nAlthough piaf made some progress, it still needs some love to be fully compliant with the [FIPA specification](http://fipa.org/repository/standardspecs.html).\n\nWe provide some examples to help you understand what is possible to create with the current version, take a look at <https://gitlab.com/ornythorinque/piaf/-/tree/master/src/piaf/examples>.\n\n### Supported features\n\n- AMS (partial, only the query function)\n- DF\n- Communications within a platform\n- Communications between two **piaf platforms** (with some limitations)\n\n### Missing features\n\n- FIPA SL support (only plain Python objects are supported)\n- Federated DF\n- Name resolution\n- "Official" envelope representations (XML, bit-efficient) and MTPs (mainly HTTP, we don\'t plan to support IIOP)\n\n## Documentation\n\nThe full documentation (both user and API) is available here: <https://ornythorinque.gitlab.io/piaf>\nIt will teach you how to install and run your own agents.\n\n## Author(s)\n\n* ornythorinque (pierredubaillay@outlook.fr)\n',
    'author': 'Pierre DUBAILLAY',
    'author_email': 'pierredubaillay@outlook.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ornythorinque/piaf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
