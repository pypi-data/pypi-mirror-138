# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrpc']

package_data = \
{'': ['*']}

install_requires = \
['case-switcher>=1.2.1,<2.0.0',
 'jsonrpc2-objects>=2.0.0,<3.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'openrpc',
    'version': '4.0.1',
    'description': 'OpenRPC provides classes to rapidly develop an OpenRPC server.',
    'long_description': '<div align=center>\n  <h1>OpenRPC</h1>\n  <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg"\n   height="20"\n   alt="License: AGPL v3">\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"\n   height="20"\n   alt="Code style: black">\n  <img src="https://img.shields.io/pypi/v/openrpc.svg"\n   height="20"\n   alt="PyPI version">\n  <img src="https://img.shields.io/badge/coverage-100%25-success"\n   height="20"\n   alt="Code Coverage">\n  <a href="https://gitlab.com/mburkard/openrpc/-/blob/main/CONTRIBUTING.md">\n    <img src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=2267a0"\n     height="20"\n     alt="Contributions Welcome">\n  </a>\n  <h3>OpenRPC provides classes to rapidly develop an\n  <a href="https://open-rpc.org">OpenRPC</a> server.</h3>\n</div>\n\n## Installation\n\nOpenRPC is on PyPI and can be installed with:\n\n```shell\npip install openrpc\n```\n\n## Usage\n\nThis library provides an `RPCServer` class that can be used to quickly\ncreate an OpenRPC Server; it needs at minimum a title and version.\n\n```python\nfrom openrpc.server import RPCServer\n\nrpc = RPCServer(title="Demo Server", version="1.0.0")\n```\n\n### Register a function as an RPC Method\n\nTo register a method with the RPCServer add the `@rpc.method` decorator\nto a function.\n\n```python\n@rpc.method\ndef add(a: int, b: int) -> int:\n    return a + b\n```\n\n### Process JSON RPC Request\n\nOpenRPC is transport agnostic. To use it, pass JSON RPC requests as\nstrings or byte strings to the `process_request` method.\n\nThe `process_request` will return a JSON RPC response as a string.\n\n```python\nreq = """\n{\n  "id": 1,\n  "method": "add",\n  "params": {"a": 2, "b": 2},\n  "jsonrpc": "2.0"\n}\n"""\nrpc.process_request(req)  # \'{"id": 1, "result": 4, "jsonrpc": "2.0}\'\n```\n\n### RPC Discover\n\nThe `rpc.discover` method is automatically generated. It relies heavily\non type hints.\n\n### Pydantic Support\n\nFor data classes to work properly use Pydantic.\nRPCServer will use Pydantic for JSON serialization/deserialization as\nwell as generating schemas when calling `rpc.discover`.\n\n### Async Support (v1.2+)\n\nRPCServer has async support:\n\n```python\nawait rpc.process_request_async(req)\n```\n\n## Example\n\n```python\nfrom flask import Flask, request\n\nfrom openrpc.server import RPCServer\n\napp = Flask(__name__)\nrpc = RPCServer(title="Demo Server", version="1.0.0")\n\n\n@rpc.method\ndef add(a: int, b: int) -> int:\n    return a + b\n\n\n@app.post("/api/v1/")\ndef process_rpc() -> str:\n    return rpc.process_request(request.data)\n\n\nif __name__ == "__main__":\n    app.run()\n```\n\nExample In\n\n```json\n[\n  {\n    "id": 1,\n    "method": "add",\n    "params": {"a": 1, "b": 3},\n    "jsonrpc": "2.0"\n  }, {\n    "id": 2,\n    "method": "add",\n    "params": [11, "thirteen"],\n    "jsonrpc": "2.0"\n  }\n]\n```\n\nExample Result Out\n\n```json\n[\n  {\n    "id": 1,\n    "result": 4,\n    "jsonrpc": "2.0"\n  }, {\n    "id": 2,\n    "error": {\n      "code": -32000,\n      "message": "TypeError: unsupported operand type(s) for +: \'int\' and \'str\'"\n    },\n    "jsonrpc": "2.0"\n  }\n]\n```\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/openrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
