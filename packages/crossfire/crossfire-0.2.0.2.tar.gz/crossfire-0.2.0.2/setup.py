# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crossfire']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'geopandas>=0.10.1,<0.11.0',
 'pandas>=1.3.3,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'crossfire',
    'version': '0.2.0.2',
    'description': 'crossfire: Download spatial data sets from crossfire project',
    'long_description': '\n<img src="https://raw.githubusercontent.com/voltdatalab/crossfire/master/crossfire_hexagono.png" width="130px" alt="hexagon crossfire"/>\n\n\n# crossfire\n\n`crossfire` is a package created to give easier access to the datasets of the project [Fogo Cruzado](https://fogocruzado.org.br/), which is a digital collaboration platform to register gun shootings in the metropolitan areas of Rio de Janeiro and Recife.\n\nThe package facilitates data extraction from the [project open-data API](https://api.fogocruzado.org.br/), developed by [Volt Data Lab](https://www.voltdata.info/en-lg).\n\n## Installing and loading the package\n\nCurrently, the `crossfire` package can be installed directly from pip:\n\n```\npip install crossfire\n```\n\n## Functions\n\n`crossfire` has 3 functions: `fogocruzado_signin`, `get_fogocruzado` and `get_cities`.\n\n* `fogocruzado_signin` is used to give access to Fogo Cruzado\'s API. To access Fogo Cruzado\'s API, [users should be registered](https://api.fogocruzado.org.br/register) and insert their e-mail and password for authentication. Thus, the function registers these information on the current R session, so that it can be used to obtain the Bearer token to extract data using the API. \n\n\n```\n>>> from crossfire import fogocruzado_signin\n>>> fogocruzado_signin(\'user@host.com\', \'password\')\n```\n\n* `get_fogocruzado` extracts slices or the whole dataset of shootings registered by Fogo Cruzado. The function returns a data frame, in which each line corresponds to a shooting registered and its information. It can also filter the data according to some parameters,  city/state - `city` and `state` -, initial and final date - `initial_date` and `final_date` -, and the presence of security forces - `security_agent`. One should note that each request using the `crossfire` package needs to be under a 210 days (roughly 7 months) time interval, from any portion of the full dataset.\n\n```\n>>> from crossfire import get_fogocruzado\n>>> fogocruzado = get_fogocruzado(state=[\'RJ\'])\n```\n\n## Other examples\n\n```\nfrom datetime import date\nfrom crossfire import fogocruzado_signin, get_fogocruzado\n\n# Extract data for all registered shootings\nfogocruzado = get_fogocruzado(()\n\n# Extract data for shootings in the cities of Rio de Janeiro and Recife in 2018\nfogocruzado_rj_recife = get_fogocruzado(\n    city = ["Rio de Janeiro, "Recife"],\n    initial_date = date(2018, 07, 01),\n    final_date = date(2018, 12, 31))\n\n# Extract data from occurents reported by the police and in which security agents were present\nfogocruzado_security = get_fogocruzado(security_agent = [1])\n```\n\n* `get_cities()` returns a `data.frame` with information about all cities from the Rio de Janeiro and Recife metropolitan areas covered by the Fogo Cruzado initiative.\n\n## More information\n\nFor more information on how the package works and for exemples on using the module, see the [tutorial](https://github.com/FelipeSBarros/crossfire_tutorial) repository.\n\n## Python module authors\n\n[Felipe Sodré Mendes Barros](https://github.com/FelipeSBarros)\n> Funding: This implementation was funded by CYTED project number 520RT0010. redGeoLIBERO\n\n## API Authors\n\n[Lucas Gelape](https://github.com/lgelape), for [Volt Data Lab](https://www.voltdata.info/en-lg).\n\n## Contributors\n\n[Sérgio Spagnuolo](https://github.com/voltdatalab), [Denisson Silva](https://github.com/silvadenisson) and [Felipe Sodré Mendes Barros](https://github.com/FelipeSBarros).\n',
    'author': 'Felipe Barros',
    'author_email': 'felipe.b4rros@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fogocruzado.org.br/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
