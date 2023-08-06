# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netatmo_geopy', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/*']}

install_requires = \
['contextily>=1.2.0,<2.0.0',
 'fire==0.4.0',
 'geopandas>=0.10.2,<0.11.0',
 'oauthlib>=3.1.1,<4.0.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'schedule>=1.1.0,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1',
          'pytest-datadir>=1.3.1,<2.0.0',
          'requests-mock>=1.9.3,<2.0.0']}

entry_points = \
{'console_scripts': ['netatmo_geopy = netatmo_geopy.cli:main']}

setup_kwargs = {
    'name': 'netatmo-geopy',
    'version': '0.1.0',
    'description': 'Pythonic package to access Netatmo CWS data.',
    'long_description': '[![PyPI version fury.io](https://badge.fury.io/py/netatmo-geopy.svg)](https://pypi.python.org/pypi/netatmo-geopy/)\n[![Documentation Status](https://readthedocs.org/projects/netatmo-geopy/badge/?version=latest)](https://netatmo-geopy.readthedocs.io/en/latest/?badge=latest)\n[![CI/CD](https://github.com/martibosch/netatmo-geopy/actions/workflows/dev.yml/badge.svg)](https://github.com/martibosch/netatmo-geopy/blob/main/.github/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/martibosch/netatmo-geopy/branch/main/graph/badge.svg?token=ZDFCCPJ6AK)](https://codecov.io/gh/martibosch/netatmo-geopy)\n[![GitHub license](https://img.shields.io/github/license/martibosch/netatmo-geopy.svg)](https://github.com/martibosch/netatmo-geopy/blob/main/LICENSE)\n\n# Netatmo GeoPy\n\n\nPythonic package to access Netatmo CWS data.\n\n```python\nimport netatmo_geopy as nat\n\nlon_sw, lat_sw, lon_ne, lat_ne = 6.5175, 46.5012, 6.7870, 46.6058\ncws_recorder = nat.CWSRecorder(lon_sw, lat_sw, lon_ne, lat_ne)\ngdf = cws_recorder.get_snapshot_gdf()\ngdf.head()\n```\n\n<div>\n    <style scoped>\n     .dataframe tbody tr th:only-of-type {\n         vertical-align: middle;\n     }\n\n     .dataframe tbody tr th {\n         vertical-align: top;\n     }\n\n     .dataframe thead th {\n         text-align: right;\n     }\n    </style>\n    <table border="1" class="dataframe">\n        <thead>\n            <tr style="text-align: right;">\n                <th></th>\n                <th>2022-02-12T19:13</th>\n                <th>geometry</th>\n            </tr>\n            <tr>\n                <th>station_id</th>\n                <th></th>\n                <th></th>\n            </tr>\n        </thead>\n        <tbody>\n            <tr>\n                <th>02:00:00:01:5e:e0</th>\n                <td>6.6</td>\n                <td>POINT (6.82799 46.47089)</td>\n            </tr>\n            <tr>\n                <th>02:00:00:22:c0:c0</th>\n                <td>4.9</td>\n                <td>POINT (6.82904 46.47005)</td>\n            </tr>\n            <tr>\n                <th>02:00:00:2f:0b:16</th>\n                <td>3.5</td>\n                <td>POINT (6.82516 46.47294)</td>\n            </tr>\n            <tr>\n                <th>02:00:00:59:00:2a</th>\n                <td>3.8</td>\n                <td>POINT (6.84547 46.46779)</td>\n            </tr>\n            <tr>\n                <th>02:00:00:52:ed:5a</th>\n                <td>3.8</td>\n                <td>POINT (6.87359 46.47067)</td>\n            </tr>\n        </tbody>\n    </table>\n</div>\n\n```python\nnat.plot_snapshot(gdf)\n```\n\n![lausanne-snapshot](https://github.com/martibosch/netatmo-geopy/blob/main/docs/figures/lausanne.png)\n\nSee [the user guide](https://martibosch.github.io/netatmo-geopy/user-guide) for a more thorough overview of netatmo-geopy.\n\n## Acknowledgements\n\n* This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Martí Bosch',
    'author_email': 'marti.bosch@epfl.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/martibosch/netatmo-geopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
