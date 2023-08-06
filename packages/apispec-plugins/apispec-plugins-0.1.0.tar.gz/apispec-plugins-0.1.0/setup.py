# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apispec_plugins', 'apispec_plugins.webframeworks']

package_data = \
{'': ['*']}

install_requires = \
['apispec[yaml]>=2.0.0,<3.0.0']

extras_require = \
{'flask': ['Flask[flask]>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'apispec-plugins',
    'version': '0.1.0',
    'description': 'Plugins for apispec',
    'long_description': '# apispec-plugins\n\n[![ci](https://github.com/rena2damas/apispec-plugins/actions/workflows/main.yaml/badge.svg)](https://github.com/rena2damas/apispec-plugins/actions/workflows/main.yaml)\n[![codecov](https://codecov.io/gh/rena2damas/apispec-plugins/branch/master/graph/badge.svg)](https://app.codecov.io/gh/rena2damas/apispec-plugins/branch/master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n[apispec](https://github.com/marshmallow-code/apispec) plugins for integrating with different components (web\nframeworks, packages, etc).\n\nCurrently supported plugins:\n\n* ```apispec_plugins.webframeworks.flask```\n\n## Installation\n\nInstall the package directly from ```PyPI``` (recommended):\n\n```bash\npip install apispec-plugins\n```\n\nPlugin dependencies like ```Flask``` are not installed with the package by default. To have ```Flask``` installed, do\nlike so:\n\n```bash\npip install apispec-plugins[flask]\n```\n\n### Migration from ```apispec<1.0.0```\n\nThe location from where plugins, like ```FlaskPlugin``` imports, are imported is different. Therefore, the imports need\nto be performed this way:\n\n```python\n# apispec<1.0.0\nfrom apispec.ext.flask import FlaskPlugin\n\n# apispec>=1.0.0\nfrom apispec_plugins.webframeworks.flask import FlaskPlugin\n```\n\n## Example Usage\n\n```python\nfrom apispec import APISpec\nfrom apispec_plugins.webframeworks.flask import FlaskPlugin\nfrom flask import Flask\n\nspec = APISpec(\n    title="Pet Store",\n    version="1.0.0",\n    openapi_version="2.0",\n    info=dict(description="A minimal pet store API"),\n    plugins=(FlaskPlugin(),),\n)\n\napp = Flask(__name__)\n\n\n@app.route("/pet/<petId>")\ndef pet(petId):\n    """Find pet by ID.\n    ---\n    get:\n        parameters:\n            - in: path\n              name: petId\n        responses:\n            200:\n                description: display pet data\n    """\n    return f"Display pet with ID {petId}"\n\n\n# Since `path` inspects the view and its route,\n# we need to be in a Flask request context\nwith app.test_request_context():\n    spec.path(view=pet)\n```\n\nAlternatively, a ```Flask``` ```MethodView``` can be used:\n\n```python\nfrom flask.views import MethodView\n\n\nclass PetAPI(MethodView):\n    def get(self, petId):\n        # get pet by ID\n        pass\n\n\napp.add_url_rule("/pet/<petId>", view_func=PetAPI.as_view("pet_view"))\n```\n\nThere is also easy integration with other packages like ```Flask-RESTful```:\n\n```python\nfrom flask_restful import Api, Resource\n\n\nclass PetAPI(Resource):\n    def get(self, petId):\n        # get pet by ID\n        pass\n\n\napi = Api(app)\napi.add_resource(PetAPI, "/pet/<petId>", endpoint="pet")\n```\n\n### Dynamic specs\n\nAs seen so far, specs are specified in the docstring of the view or class. However, with the ```spec_from``` decorator,\none can dynamically set specs:\n\n```python\nfrom apispec_plugins import spec_from\n\n\n@spec_from(\n    {\n        "parameters": {"in": "path", "name": "petId"},\n        "responses": {200: {"description": "display pet data"}},\n    }\n)\ndef pet(petID):\n    """Find pet by ID."""\n    pass\n```\n\n## Why not ```apispec-webframeworks```?\n\nThe conceiving of this project was based\non [apispec-webframeworks](https://github.com/marshmallow-code/apispec-webframeworks). While that project is focused on\nintegrating web frameworks with ```APISpec```, this repository goes a step further in providing the best integration\npossible with the ```APISpec``` standards. Some limitations on that project were also addressed, like:\n\n* a path cannot register no more than 1 single rule per endpoint;\n* support for additional libraries like ```Flask-RESTful```;\n* limited docstring spec processing;\n\n## Tests & linting\n\nRun tests with ```tox```:\n\n```bash\n# ensure tox is installed\n$ tox\n```\n\nRun linter only:\n\n```bash\n$ tox -e lint\n```\n\nOptionally, run coverage as well with:\n\n```bash\n$ tox -e coverage\n```\n\n## License\n\nMIT licensed. See [LICENSE](LICENSE).\n',
    'author': 'Renato Damas',
    'author_email': 'rena2damas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rena2damas/apispec-plugins',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
