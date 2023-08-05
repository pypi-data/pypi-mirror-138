# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stkclient']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0', 'rsa>=4.8,<5.0']

entry_points = \
{'console_scripts': ['stkclient = stkclient.__main__:main']}

setup_kwargs = {
    'name': 'stkclient',
    'version': '0.1.1',
    'description': 'Send To Kindle',
    'long_description': 'Send To Kindle\n==============\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/stkclient.svg\n   :target: https://pypi.org/project/stkclient/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/stkclient.svg\n   :target: https://pypi.org/project/stkclient/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/stkclient\n   :target: https://pypi.org/project/stkclient\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/stkclient\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/stkclient/latest.svg?label=Read%20the%20Docs\n   :target: https://stkclient.readthedocs.io/\n   :alt: Read the documentation at https://stkclient.readthedocs.io/\n.. |Tests| image:: https://github.com/maxdjohnson/stkclient/workflows/Tests/badge.svg\n   :target: https://github.com/maxdjohnson/stkclient/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/maxdjohnson/stkclient/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/maxdjohnson/stkclient\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\n``stkclient`` implements a client for amazon\'s "Send to Kindle" service. It allows python programs to\nsend files to a kindle device without the 10mb limit that applies to email files.\n\nFeatures\n--------\n\n* OAuth-based authorization\n* Send large (>10MB) files to Kindle devices\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Send To Kindle* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install stkclient\n\n\nCreating a Client\n-----------------\n\nTo create a client, you must authenticate the user. Currently the only supported authentication mechanism is OAuth2:\n\n.. code:: python\n\n   import stkclient\n\n   a = stkclient.OAuth2()\n   signin_url = a.get_signin_url()\n   # Open `signin_url` in a browser, sign in and authorize the application, pass\n   # the final redirect_url below\n   client = a.create_client(redirect_url)\n\nOnce a client is created, it can be serialized and deserialized using ``Client.load`` / ``Client.loads`` and ``client.dump`` / ``client.dumps``\n\n.. code:: python\n\n   with open(\'client.json\', \'w\') as f:\n       client.dump(f)\n   with open(\'client.json\', \'r\') as f:\n       client = stkclient.Client.load(f)\n\n\nSending a File\n--------------\n\nOnce you have a Client object, you can list devices and send files to specified devices.\n\n.. code:: python\n\n   devices = client.get_owned_devices()\n   destinations = [d.device_serial_number for d in devices.owned_devices]\n   client.send_file(filepath, destinations, author=author, title=title)\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Send To Kindle* is free and open source software.\n\n\nCredits\n-------\n\nProject structure from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n',
    'author': 'Max Johnson',
    'author_email': 'maxdjohnson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxdjohnson/stkclient',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
