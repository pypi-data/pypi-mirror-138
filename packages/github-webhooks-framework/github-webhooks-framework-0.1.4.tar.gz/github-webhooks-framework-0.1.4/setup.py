# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['github_webhooks', 'github_webhooks.handlers', 'github_webhooks.schemas']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.73.0,<0.74.0', 'pydantic[dotenv]>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'github-webhooks-framework',
    'version': '0.1.4',
    'description': 'GitHub Webhooks Framework',
    'long_description': "# Python GitHub Webhooks Framework\n\nSimple and lightweight micro framework for quick integration with [GitHub\nwebhooks][1].  \nIt's based on [FastAPI][3] and [pydantic][4], nothing more!  \nAsync and mypy friendly. \n\n[![Run CI](https://github.com/karech/github-webhooks/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/karech/github-webhooks/actions/workflows/ci.yml)  \n[![PyPI](https://img.shields.io/pypi/v/github-webhooks-framework.svg)][2]\n\n\n## Installation\nJust add `github-webhooks-framework` package.   \nExample: \n* `pip install github-webhooks-framework`\n* `poetry add github-webhooks-framework`\n\n\n## Example\nCreate file `example.py` and copy next code:\n```python\nimport uvicorn\nfrom pydantic import BaseModel\n\nfrom github_webhooks import create_app\nfrom github_webhooks.schemas import WebhookCommonPayload\n\n\n# WebhookCommonPayload is based on pydantic.BaseModel\nclass PullRequestPayload(WebhookCommonPayload):\n    class Pull(BaseModel):\n        title: str\n        url: str\n    \n    action: str\n    pull_request: Pull\n    \n\n# Initialize Webhook App\napp = create_app()\n\n\n# Register webhook handler:\n#   `pull_request` - name of an event to handle\n#   `PullRequestPayload` - webhook payload will be parsed into this model\n@app.hooks.register('pull_request', PullRequestPayload)\nasync def handler(payload: PullRequestPayload) -> None:\n    print(f'New pull request {payload.pull_request.title}')\n    print(f'  link: {payload.pull_request.url}')\n    print(f'  author: {payload.sender.login}')\n\n\nif __name__ == '__main__':\n    # start uvicorn server\n    uvicorn.run(app)\n```\n  \n \n### Let's have detailed overview. \n\nWe start by defining payload [Model][5] to parse incoming [Pull Request Body][6]. \n```python\nclass PullRequestPayload(WebhookCommonPayload):\n    class Pull(BaseModel):\n        title: str\n        url: str\n    \n    action: str\n    pull_request: Pull\n```\nIn this example we only want to get `action`, `pull_request.title` and `pull_request.url` from payload.  \nBy subclassing `WebhookCommonPayload` model will automatically get `sender`, `repository` and `organization` fields.\n\n\nNext - we are creating ASGI app (based on FastAPI app)\n```python\napp = create_app()\n```\nOptionally we can provide here `secret_token` [Github Webhook secret][7]\n```python\napp = create_app(secret_token='super-secret-token')\n```\n\nAnd time to define our handler\n```python\n@app.hooks.register('pull_request', PullRequestPayload)\nasync def handler(payload: PullRequestPayload) -> None:\n    print(f'New pull request {payload.pull_request.title}')\n    print(f'  link: {payload.pull_request.url}')\n    print(f'  author: {payload.sender.login}')\n```\n\nWe are using here `@app.hooks.register` deco, which accepts 2 arguments:\n* `event: str` - name of webhook event\n* `payload_cls: pydantic.BaseModel` - pydantic model class to parse request, subclassed from `pydantic.BaseModel` \nor `WebhookCommonPayload`.\n\nAnd our handler function must be any of this signatures:  \n```python\nasync def handler(payload: PullRequestPayload) -> None:\n    ...\n```\n```python\nasync def handler(payload: PullRequestPayload, headers: WebhookHeaders) -> Optional[str]:\n    # `headers` will be WebhookHeaders model with Github Webhook headers parsed.\n    ...\n```  \n\n\nAnd the last - let's launch it.  \nFor example with uvicorn  \n```shell\nuvicorn example:app\n```\nWebhook will be available on http://localhost:8000/hook\n\nThat's it!\nNow you have a webhook server, which can handle incoming Github Webhook requests.\n\n\n\n[1]: https://developer.github.com/webhooks/\n[2]: https://pypi.python.org/pypi/github-webhooks-framework\n[3]: https://fastapi.tiangolo.com/\n[4]: https://pydantic-docs.helpmanual.io/\n[5]: https://pydantic-docs.helpmanual.io/usage/models/\n[6]: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#pull_request\n[7]: https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks\n",
    'author': 'karech',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/karech/github-webhooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
