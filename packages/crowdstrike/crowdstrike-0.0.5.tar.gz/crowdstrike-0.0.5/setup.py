# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crowdstrike']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'requests-oauthlib>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'crowdstrike',
    'version': '0.0.5',
    'description': 'Python interface to the Crowdstrike API',
    'long_description': '* THIS IS NO LONGER UPDATED *\n\n\n# Crowdstrike API\n\nImplements some of the functions to interface with the [Crowdstrike APIs](https://assets.falcon.crowdstrike.com/support/api/swagger.html).\n\nWant to contribute? Log an issue or PR on the Repo.\n\nTo enable logging, use [loguru](https://github.com/Delgan/loguru) and run `logger.enable("crowdstrike")` in your script.\n\n## Checking that all the endpoints are covered\n\n`validate_api_endpoints.py` needs the `swagger.json` file from the documentation page on [crowdstrike.com](https://assets.falcon.crowdstrike.com/support/api/swagger.html), then you can check everything has an actionable method.\n\nEg:\n\n    2020-10-14 18:56:57.801 | INFO     | __main__:<module>:60 - [OK] create_rtr_session() implements /real-time-response/entities/sessions/v1 : post\n    2020-10-14 18:56:57.801 | INFO     | __main__:<module>:60 - [OK] delete_rtr_session() implements /real-time-response/entities/sessions/v1 : delete\n    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /real-time-response/queries/put-files/v1 : get\n    2020-10-14 18:56:57.802 | INFO     | __main__:<module>:60 - [OK] search_rtr_scripts() implements /real-time-response/queries/scripts/v1 : get\n    2020-10-14 18:56:57.802 | INFO     | __main__:<module>:60 - [OK] list_rtr_session_ids() implements /real-time-response/queries/sessions/v1 : get\n    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /samples/entities/samples/v2 : post\n    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /sensors/combined/installers/v1 : get\n    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /sensors/entities/datafeed-actions/v1/{partition} : post\n    2020-10-14 18:56:57.803 | ERROR    | __main__:<module>:64 - Path not found /sensors/entities/datafeed/v2 : get\n    2020-10-14 18:56:57.803 | ERROR    | __main__:<module>:64 - Path not found /sensors/entities/download-installer/v1 : get\n\n... lots to do.',
    'author': 'James Hodgkinson',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yaleman/crowdstrike_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
