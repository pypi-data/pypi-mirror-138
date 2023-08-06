# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_ratelimiter']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.1,<3.0.0', 'fastapi>=0.73.0,<0.74.0']

setup_kwargs = {
    'name': 'fastapi-ratelimiter',
    'version': '0.0.1',
    'description': 'Redis-based rate-limiting for FastAPI',
    'long_description': '# FastAPI Ratelimiter\n\n[![PyPI version](https://img.shields.io/pypi/v/fastapi-ratelimiter.svg)]\n\n**Documentation**: https://fastapi-ratelimit.readthedocs.io/en/latest/ \n\n## Quick start:\n\n```python\n\nimport asyncio\n\nimport aioredis\nimport uvicorn\nfrom fastapi import FastAPI, Depends\nfrom starlette.responses import JSONResponse\n\nfrom fastapi_ratelimiter import RateLimited, RedisDependencyMarker\nfrom fastapi_ratelimiter.strategies import BucketingRateLimitStrategy\n\napp = FastAPI()\nredis = aioredis.from_url("redis://localhost", decode_responses=True, encoding="utf-8")\n\n\n@app.get(\n    "/some_expensive_call", response_class=JSONResponse,\n    dependencies=[\n        Depends(RateLimited(BucketingRateLimitStrategy(rate="10/60s")))\n    ]\n)\nasync def handle_test_endpoint():\n    await asyncio.sleep(5)\n    return {"hello": "world"}\n\n\napp.dependency_overrides[RedisDependencyMarker] = lambda: redis\n\nuvicorn.run(app)\n\n```',
    'author': 'GLEF1X',
    'author_email': None,
    'maintainer': 'GLEF1X',
    'maintainer_email': 'glebgar567@gmail.com',
    'url': 'https://github.com/GLEF1X/fastapi-ratelimit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
