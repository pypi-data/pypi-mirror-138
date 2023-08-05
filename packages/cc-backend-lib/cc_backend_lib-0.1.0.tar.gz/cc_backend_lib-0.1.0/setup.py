# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cc_backend_lib',
 'cc_backend_lib.cache',
 'cc_backend_lib.clients',
 'cc_backend_lib.errors',
 'cc_backend_lib.models']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'geojson-pydantic>=0.3.1,<0.4.0',
 'pydantic>=1.9.0,<2.0.0',
 'redis>=4.1.2,<5.0.0',
 'toolz>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'cc-backend-lib',
    'version': '0.1.0',
    'description': 'A library with classes and types used througout the backend for Conflict Cartographer',
    'long_description': '\n# CC Backend Client\n\nThis library contains several classes and data models that are useful when\nwriting services that interact with other services in Conflict Cartographer. In\nparticular, the modules `api_client` and `schema` respectively provide classes\nfor retrieving and modelling data from APIs.\n\n## Data retrieval\n\nData retrieval is offered via the `cc_backend_lib.dal.Dal` class. This class is\ninstantiated by passing several API clients: \n\n```\nfrom cc_backend_lib.clients import predictions_client, scheduler_client, users_client, countries_client\nfrom cc_backend_lib import dal\n\ncc_dal = dal.Dal(\n      predictions = predictions_client.PredictionsClient(...),\n      scheduler = scheduler_client.SchedulerClient(...),\n      users = users_client.UsersClient(...),\n      countries = countries_client.CountriesClient(...),\n   )\n```\n\nThe class has several methods that offer access to data and summaries. See `help(Dal)`\n',
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/prio-data/cc_backend_lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
