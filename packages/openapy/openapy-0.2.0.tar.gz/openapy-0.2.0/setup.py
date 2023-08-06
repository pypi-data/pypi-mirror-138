# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapy']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'single-source>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['openapy = openapy.main:main']}

setup_kwargs = {
    'name': 'openapy',
    'version': '0.2.0',
    'description': '',
    'long_description': '![openapy Logo](https://raw.githubusercontent.com/edge-minato/openapy/main/doc/img/logo.jpg)\n\n\n[![pypi version](https://img.shields.io/pypi/v/openapy.svg?style=flat)](https://pypi.org/pypi/openapy/)\n[![python versions](https://img.shields.io/pypi/pyversions/openapy.svg?style=flat)](https://pypi.org/pypi/openapy/)\n[![license](https://img.shields.io/pypi/l/openapy.svg?style=flat)](https://github.com/edge-minato/openapy/blob/master/LICENSE)\n[![Unittest](https://github.com/edge-minato/openapy/actions/workflows/unittest.yml/badge.svg)](https://github.com/edge-minato/openapy/actions/workflows/unittest.yml)\n[![codecov](https://codecov.io/gh/edge-minato/openapy/branch/main/graph/badge.svg?token=YDZAMKUNS0)](https://codecov.io/gh/edge-minato/openapy)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black")\n[![Downloads](https://pepy.tech/badge/openapy)](https://pepy.tech/project/openapy)\n[![Downloads](https://pepy.tech/badge/openapy/week)](https://pepy.tech/project/openapy)\n\n`openapy` adds CI/CD capability to [OpenAPI generator](https://github.com/OpenAPITools/openapi-generator)\n\n\n## Overview\n\n## Quick start\n\n### With Docker\n\n```\ndocker run\n```\n\n### With Installation\n\n```\npip install openapy\n```\n\n## USAGE\n\n```\n> openapy -h\nusage: openapy [-h] [--src SRC] [--template TEMPLATE] [--all] [--version]\n\nAdditional files generator for openapi\n\noptions:\n  -h, --help            show this help message and exit\n  --src SRC, -s SRC     source dir path\n  --template TEMPLATE, -t TEMPLATE\n                        file path of the processor template\n  --all, -a             whether overwrite all files or not\n  --version, -v         show version\n```\n\n## Options\n\n(*) means it is a required option.\n\n- **src** (*): Path to the source directory that contains apis\n- **template**: Path to the custom template file\n- **all**: With this option, all files will be overwritten\n\n## Custom Template\n\nFollowing variables with `{}` brackets are available.\n\n- **IMPORTS**: All of imports of the source file like `import X`, `from X import Y`\n- **ASSIGNS**: All assigns of the source file like `var = "string"`\n- **DEF**: `async def` or `def` of the function\n- **NAME**: The function name\n- **ARGS**: Arguments of the function with type annotations\n- **RETURN_TYPE**: A type annotation for the return of the function\n- **COMMENT**: A comment inside of the function\n- **BODY**: A body of the function, like assign statement\n- **RETURN**: A return statement of the function\n\n\n### Example\n\n\n**apis/user_api.py**\n\n```python\nfrom typing import Any, Dict, List, Optional, Union  # noqa: F401\nfrom fastapi import APIRouter\nfrom openapi_server.model.user import User\n\nrouter = APIRouter()\n\n@router.post("/get_user", tags=["user"], summary="get user")\nasync def get_user(id: int) -> User:\n    """This function returns a new user"""\n    return processor.get_user.process()\n\n@router.post("/delete_user", tags=["user"], summary="delete user")\nasync def delete_user(id: int, password:str="default_password") -> bool:\n    """This function deletes user and return the result"""\n    return processor.delete_user.process()\n```\n\n**Custom Template: template.txt**\n\n```\n# coding: utf-8\n\n{IMPORTS}\n\ndef process({ARGS}) -> {RETURN_TYPE}:\n    # Implement me!\n    ...\n```\n\n**processor/get_user.py**\n\n```python\n# coding: utf-8\n\nfrom typing import Any, Dict, List, Optional, Union  # noqa: F401\nfrom fastapi import APIRouter  # noqa: F401\nfrom openapi_server.model.user import User  # noqa: F401\n\ndef process(id: int) -> User:\n    # Implement me!\n    ...\n```\n\n**processor/delete_user.py**\n\n```python\n# coding: utf-8\n\nfrom typing import Any, Dict, List, Optional, Union  # noqa: F401\nfrom fastapi import APIRouter  # noqa: F401\nfrom openapi_server.model.user import User  # noqa: F401\n\ndef process(id: int) -> User:\n    # Implement me!\n    ...\n```\n',
    'author': 'edge-minato',
    'author_email': 'edge.minato@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/edge-minato/openapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
