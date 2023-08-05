# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.apps.cache',
 'understory.apps.cache.templates',
 'understory.apps.data',
 'understory.apps.data.templates',
 'understory.apps.jobs',
 'understory.apps.jobs.templates',
 'understory.apps.owner',
 'understory.apps.owner.templates',
 'understory.apps.providers',
 'understory.apps.providers.templates',
 'understory.apps.search',
 'understory.apps.search.templates',
 'understory.apps.sites',
 'understory.apps.sites.templates',
 'understory.apps.system',
 'understory.apps.system.templates',
 'understory.host',
 'understory.host.templates',
 'understory.mkdn',
 'understory.mm',
 'understory.silos',
 'understory.uri',
 'understory.web',
 'understory.web.framework',
 'understory.web.framework.templates',
 'understory.web.headers',
 'understory.web.response']

package_data = \
{'': ['*'],
 'understory.web.framework': ['static/braid.js',
                              'static/braid.js',
                              'static/braid.js',
                              'static/braid.js',
                              'static/braid.js',
                              'static/logos/*',
                              'static/orchid.js',
                              'static/orchid.js',
                              'static/orchid.js',
                              'static/orchid.js',
                              'static/orchid.js',
                              'static/roots.js',
                              'static/roots.js',
                              'static/roots.js',
                              'static/roots.js',
                              'static/roots.js',
                              'static/solarized.css',
                              'static/solarized.css',
                              'static/solarized.css',
                              'static/solarized.css',
                              'static/solarized.css',
                              'static/understory.js',
                              'static/understory.js',
                              'static/understory.js',
                              'static/understory.js',
                              'static/understory.js']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'PyVirtualDisplay>=2.2,<3.0',
 'Pygments>=2.9.0,<3.0.0',
 'Unidecode>=1.2.0,<2.0.0',
 'acme-tiny>=4.1.0,<5.0.0',
 'argcomplete>=1.12.3,<2.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'cssselect>=1.1.0,<2.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'emoji>=1.2.0,<2.0.0',
 'feedparser>=6.0.8,<7.0.0',
 'gevent>=21.1.2,<22.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'hstspreload>=2021.7.5,<2022.0.0',
 'httpagentparser>=1.9.1,<2.0.0',
 'jsonpatch>=1.32,<2.0',
 'lxml>=4.6.3,<5.0.0',
 'microformats>=0,<1',
 'mimeparse>=0.1.3,<0.2.0',
 'pendulum>=2.1.2,<3.0.0',
 'pycryptodome>=3.10.1,<4.0.0',
 'pyscreenshot>=3.0,<4.0',
 'redis>=3.5.3,<4.0.0',
 'regex>=2021.7.6,<2022.0.0',
 'requests[socks]>=2.27.1,<3.0.0',
 'rich>=10.7.0,<11.0.0',
 'selenium>=4.1.0,<5.0.0',
 'semver>=2.13.0,<3.0.0',
 'vobject>=0.9.6,<0.10.0',
 'waitress>=2.0.0,<3.0.0',
 'watchdog>=2.1.3,<3.0.0']

entry_points = \
{'console_scripts': ['loveliness = understory.loveliness:main',
                     'web = understory.web.__main__:main']}

setup_kwargs = {
    'name': 'understory',
    'version': '0.0.90',
    'description': 'Social web framework.',
    'long_description': '# understory\n\nSocial web framework\n\n## Use\n\n### A simple website\n\n    pip install understory\n\nCreate a directory for your website (eg. `mysite/`) and place the following in\nthe package\'s `__init__.py` (eg. `mysite/__init__.py`):\n\n```python\nfrom understory import web\n\napp = web.application(__name__)\n\n@app.control("")\nclass Landing:\n    def get(self):\n        return "peaches"\n```\n\n    web serve mysite\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
