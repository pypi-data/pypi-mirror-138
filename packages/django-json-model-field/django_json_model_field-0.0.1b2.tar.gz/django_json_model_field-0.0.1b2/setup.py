# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_json_model_field',
 'django_json_model_field.db',
 'django_json_model_field.db.models',
 'django_json_model_field.forms']

package_data = \
{'': ['*'],
 'django_json_model_field': ['templates/django_json_model/forms/widgets/*']}

install_requires = \
['Django>=2.2,<3.0',
 'django-jsonfield-backport>=1.0.4,<1.1.0',
 'django-mysql>=4.5.0,<4.6.0',
 'mysqlclient>=2.1.0,<2.2.0',
 'pytest>=7.0.1,<8.0.0',
 'wheel>=0.37.1,<0.38.0']

setup_kwargs = {
    'name': 'django-json-model-field',
    'version': '0.0.1b2',
    'description': 'Use a model class to provide a strict data structure for JSON fields',
    'long_description': None,
    'author': 'Daniel Schaffer',
    'author_email': 'dschaffer@instawork.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.9',
}


setup(**setup_kwargs)
