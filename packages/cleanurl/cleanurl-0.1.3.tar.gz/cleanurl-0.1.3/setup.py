# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['cleanurl']
setup_kwargs = {
    'name': 'cleanurl',
    'version': '0.1.3',
    'description': 'Removes clutter from URLs and returns a canonicalized version',
    'long_description': "# cleanurl\nRemoves clutter from URLs and returns a canonicalized version\n\n# Install\n```\npip install cleanurl\n```\nor if you're using poetry:\n```\npoetry add cleanurl\n```\n\n# Usage\nBy default *cleanurl* retuns a cleaned URL without respecting semantics.\nFor example:\n\n```\n>>> import cleanurl\n>>> r = cleanurl.cleanurl('https://www.xojoc.pw/blog/focus.html?utm_content=buffercf3b2&utm_medium=social&utm_source=snapchat.com&utm_campaign=buffe')\n>>> r.url\n'https://xojoc.pw/blog/focus'\n>>> r.parsed_url\nParseResult(scheme='https', netloc='xojoc.pw', path='/blog/focus', params='', query='', fragment='')\n```\n\nThe default parameters are useful if you want to get a *canonical* URL without caring if the resulting URL is still valid.\n\nIf you want to get a clean URL which is still valid call it like this:\n\n```\n>>> r = cleanurl.cleanurl('https://www.xojoc.pw/blog/////focus.html', respect_semantics=True)\n>>> r.url\n'https://xojoc.pw/blog/focus.html'\n```\n\n\nFor more examples see the [unit tests](https://github.com/xojoc/cleanurl/blob/main/src/test_cleanurl.py).\n\n# Why?\nWhile there are some libraries that handle general cases, this library has website specific rules that more aggresivly normalize urls.\n\n# Users\nInitially used for [discu.eu](https://discu.eu).\n\n# Who?\n*cleanurl* was written by [Alexandru Cojocaru](https://xojoc.pw).\n\n\n# License\n*cleanurl* is [Free Software](https://www.gnu.org/philosophy/free-sw.html) and is released as [AGPLv3](https://github.com/xojoc/cleanurl/blob/main/LICENSE)",
    'author': 'Alexandru Cojocaru',
    'author_email': 'hi@xojoc.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xojoc/cleanurl',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
