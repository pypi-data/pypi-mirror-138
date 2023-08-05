# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ga', 'ga.auth', 'ga.exceptions', 'ga.model', 'ga.persist', 'ga.utils']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1.7.0,<2.0.0',
 'azure-storage-blob>=12.9.0,<13.0.0',
 'google-auth>=1.30.0,<2.0.0',
 'google-cloud-bigquery>=2.26.0,<3.0.0',
 'google-cloud-storage>=1.42.2,<2.0.0',
 'google-cloud>=0.34.0,<0.35.0',
 'requests>=2.25.1,<3.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'p360-ga-downloader',
    'version': '0.2.3',
    'description': 'Extractor for Google analytics',
    'long_description': '# Name: Persona 360 Google Analytics 360\n\n## Short description: Component, using Google Analytics API, allows you to download raw data used in Persona360 service.\n\nLong Description: This component uses the Google Analytics API to extract raw data via BigQuery and Google Cloud Platfom storage to your define storage. These data are used in Persona360 service.\nData are extracted incrementally.\nTo configure this extractor, you need to have Google Cloud Platform storage and  appropriate credentials.',
    'author': 'Roman Novosad',
    'author_email': 'roman.novosad@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DataSentics/GA_Extractor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10.0',
}


setup(**setup_kwargs)
