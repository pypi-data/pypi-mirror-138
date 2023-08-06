# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodownloads']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiodownloads',
    'version': '0.1.0',
    'description': 'Asynchronous downloads',
    'long_description': "# aiodownloads\n\nAsynchronous downloads\n\n## Usage\n\nInherit `aiodownloads.Downloader` then override handle_success, handle_fail methods\n\n## Examples\n\n- Download list of urls\n\n```python\nimport asyncio\n\nfrom aiodownloads import Downloader\n\nurls = [\n    'https://httpbin.org/status/200',\n    'https://httpbin.org/status/400'\n]\nclass UrlsDownloader(Downloader):\n\n    async def handle_success(self, resp, item):\n        content = await resp.read()\n        # save content stuff\n\n    async def handle_fail(self, resp, item):\n        ...\n\nurl_downloader = UrlsDownloader()\nasyncio.run(url_downloader.download(urls))\n```\n",
    'author': 'tinnguyen121221',
    'author_email': 'tinnguyen121221@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tinnguyentg/aiodownloads',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
