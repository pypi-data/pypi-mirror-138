# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freekassa', 'freekassa.models', 'freekassa.type']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'freekassa',
    'version': '0.1.4',
    'description': 'FreeKassa Api',
    'long_description': '# FreeKassa - Api\n\n## Intallation\n\n```json\npip install freekassa\n```\n\n## Usage\n\n### Generate link payment\n\n```python\nmerchant = Merchant(shop_id=123456789,\n                    secret1="secret1",\n                    secret2="secret2",\n                    api_key="api_key")\npayment_link = merchant.get_payment_form_url(amount=100, order_id="Product 1", us_={\'token\':\'token1\',"token2":"token2"})\n```\n\n### Check balance\n\n```python\nbalance = merchant.get_balance()\n```',
    'author': 'odi1n',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/odi1n/freekassa_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
