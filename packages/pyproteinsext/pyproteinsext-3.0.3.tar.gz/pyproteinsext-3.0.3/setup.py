# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyproteinsext', 'pyproteinsext.database', 'pyproteinsext.services.uniprot']

package_data = \
{'': ['*'],
 'pyproteinsext': ['notebooks/*',
                   'notebooks/.ipynb_checkpoints/*',
                   'notebooks/data/*']}

install_requires = \
['biopython>=1.79,<2.0',
 'bs4>=0.0.1,<0.0.2',
 'networkx>=2.6.3,<3.0.0',
 'pyproteins>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'pyproteinsext',
    'version': '3.0.3',
    'description': "'Extending pyproteins for bioinformatics tools&services'",
    'long_description': None,
    'author': 'glaunay',
    'author_email': 'pitooon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
