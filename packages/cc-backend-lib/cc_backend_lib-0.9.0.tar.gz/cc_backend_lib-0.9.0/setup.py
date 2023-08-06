# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cc_backend_lib',
 'cc_backend_lib.cache',
 'cc_backend_lib.clients',
 'cc_backend_lib.email',
 'cc_backend_lib.errors',
 'cc_backend_lib.models']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'email-validator>=1.1.3,<2.0.0',
 'geojson-pydantic>=0.3.1,<0.4.0',
 'mailjet-rest>=1.3.4,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'redis>=4.1.2,<5.0.0',
 'toolz>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'cc-backend-lib',
    'version': '0.9.0',
    'description': 'A library with classes and types used througout the backend for Conflict Cartographer',
    'long_description': '\n# CC Backend Library \n\n![tests status](https://github.com/prio-data/cc_backend_lib/actions/workflows/test.yml/badge.svg)\n\nThis library contains several classes and data models that are useful when\nwriting services that interact with other services in Conflict Cartographer. In\nparticular, the modules `api_client` and `schema` respectively provide classes\nfor retrieving and modelling data from APIs.\n\n## Data retrieval\n\nData retrieval is offered via the `cc_backend_lib.dal.Dal` class. This class is\ninstantiated by passing several API clients: \n\n```\nfrom cc_backend_lib.clients import predictions_client, scheduler_client, users_client, countries_client\nfrom cc_backend_lib import dal\n\ncc_dal = dal.Dal(\n      predictions = predictions_client.PredictionsClient(...),\n      scheduler = scheduler_client.SchedulerClient(...),\n      users = users_client.UsersClient(...),\n      countries = countries_client.CountriesClient(...),\n   )\n```\n\nThe class has several methods that offer access to data and summaries. See\n`help(Dal)`.  The `.participation_summary` method caches results for past\n(shift < 0) time-periods for efficiency.\n\n## Caching\n\nA powerful caching decorator is provided that lets you decorate both sync and\nasync functions for caching. For using different kinds of backends or for other\nkinds of customization (LRU, etc.), the caching decorator lets you pass a\ncustom cache class. There are some provided cache classes, including one that\nuses Redis: \n\n```\nfrom cc_backend_lib.cache import redis_cache, cache\n\n@cache.cache(redis_cache.RedisBackend, host = "...", expiry_time = 100)\ndef my_slow_function(a,b,c):\n   ...\n\n# First time slow\na = my_slow_function(1,2,3)\n\n# Second time fast\nb = my_slow_function(1,2,3)\n\nassert a == b\n```\n',
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
