# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['purchase',
 'purchase.controllers',
 'purchase.loggers',
 'purchase.migrations',
 'purchase.models',
 'purchase.serializers',
 'purchase.strings',
 'purchase.templates',
 'purchase.verifiers',
 'purchase.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.7,<4.0.0',
 'Pygments>=2.10.0,<3.0.0',
 'django-admin-rangefilter>=0.8.1,<0.9.0',
 'django-filter>=2.4.0,<3.0.0',
 'djangorestframework>=3.12.4,<4.0.0',
 'google-api-python-client>=2.21.0,<3.0.0',
 'google-auth-oauthlib>=0.4.6,<0.5.0',
 'google-auth>=2.1.0,<3.0.0',
 'google>=3.0.0,<4.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'django-purchase-core',
    'version': '0.1.4',
    'description': 'A reusable Django app for creating, logging and verifying purchases.',
    'long_description': 'Purchase Core\n===============\n\nA reusable Django app for creating, logging and verifying purchases.\n\nQuick start\n-----------\n\n1. Install Django Purchase Core & Dependancies:\n\n    >>> pip install django-purchase-core\n\n\n2. Add "purchase", "rest_framework\', and "rangefilter" to your INSTALLED_APPS setting like this:\n\n.. code:: python\n\n        INSTALLED_APPS = [\n            ...,\n            \'rest_framework\',\n            \'purchase\',\n            \'rangefilter\',\n            ...,\n        ]\n\n3. Add the following to app_config.urls:\n\n.. code:: python\n\n    from django.conf.urls import url, include\n\n    urlpatterns = [\n        ...,\n        path("api/", include("purchase.urls")),\n        ...,\n    ]\n\n\n4. Run Django Commands:\n\n    >>> python manage.py makemigrations\n    >>> python manage.py migrate\n\n\n5. Configure configuration and credentials for your game in the admin panel.\n\nAdd progress level update processing\n-------------------------------------\n\n1. Set update_player_progress_class in ProcessPurchaseView\n\n.. code:: python\n\n        from purchase.view import ProcessPurchaseView\n        from my_app import UpdateClass\n\n        class ProcessPurchaseViewWithUpdate(ProcessPurchaseView):\n            update_player_progress_class = UpdateClass\n\n2. Describe the player\'s update logic in the update_player_progress method\n\n.. code:: python\n\n        from purchase.view import ProcessPurchaseView\n        from my_app import UpdateClass\n\n        class ProcessPurchaseViewWithUpdate(ProcessPurchaseView):\n            update_player_progress_class = UpdateClass\n\n            def update_player_progress(self):\n                handler = self.update_player_progress_class()\n                handler.update_player_progress()\n',
    'author': 'Qmobi',
    'author_email': 'info@qmobi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/boy-scouts/game-core-purchase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
