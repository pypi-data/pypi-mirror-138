# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omicidx',
 'omicidx.geo',
 'omicidx.ontologies',
 'omicidx.scripts',
 'omicidx.sra']

package_data = \
{'': ['*']}

install_requires = \
['Click',
 'aiohttp>=3.6.2,<4.0.0',
 'biopython==1.75',
 'boto3>=1.9,<2.0',
 'gcsfs>=0.8.0,<0.9.0',
 'pronto>=2.4.4,<3.0.0',
 'pydantic',
 'requests>=2.22,<3.0',
 'sd_cloud_utils',
 'sphinx_click>=2.3.2,<3.0.0']

entry_points = \
{'console_scripts': ['omicidx_tool = omicidx.scripts.cli:cli']}

setup_kwargs = {
    'name': 'omicidx',
    'version': '1.2.0',
    'description': 'The OmicIDX project collects, reprocesses, and then republishes metadata from multiple public genomics repositories. Included are the NCBI SRA, Biosample, and GEO databases. Publication is via the cloud data warehouse platform Bigquery, a set of performant search and retrieval APIs, and a set of json-format files for easy incorporation into other projects.',
    'long_description': '',
    'author': 'Sean Davis',
    'author_email': 'seandavi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omicidx/omicidx-parsers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
