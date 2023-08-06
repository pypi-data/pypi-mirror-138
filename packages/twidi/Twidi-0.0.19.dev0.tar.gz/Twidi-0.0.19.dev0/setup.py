# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['twidi',
 'twidi.admin',
 'twidi.admin.views',
 'twidi.device',
 'twidi.logger',
 'twidi.twitch']

package_data = \
{'': ['*'], 'twidi.admin': ['data/*', 'static/*', 'templates/*']}

install_requires = \
['Flask-Admin>=1.5.8,<2.0.0',
 'Flask-DebugToolbar>=0.11.0,<0.12.0',
 'Flask-SQLAlchemy>=2.5.1,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'SQLAlchemy-Utils>=0.38.2,<0.39.0',
 'SQLAlchemy>=1.4.31,<2.0.0',
 'black>=21.12b0,<22.0',
 'cleo>=0.8.1,<0.9.0',
 'fire>=0.4.0,<0.5.0',
 'mido>=1.2.10,<2.0.0',
 'pygame>=2.1.2,<3.0.0',
 'pytest>=6.2.5,<7.0.0',
 'twitchio>=2.1.4,<3.0.0',
 'yamlable>=1.0.4,<2.0.0']

entry_points = \
{'console_scripts': ['twidi = twidi.__main__:main']}

setup_kwargs = {
    'name': 'twidi',
    'version': '0.0.19.dev0',
    'description': 'Creates a simple bridge between Twitch chat commands and MIDI controls',
    'long_description': None,
    'author': 'Greg Hatt',
    'author_email': 'ghattjr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
