# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_bravado']
install_requires = \
['bravado>=11.0.2,<12.0.0', 'nested_lookup==0.2.22']

entry_points = \
{'pytest11': ['bravado = pytest_bravado']}

setup_kwargs = {
    'name': 'pytest-bravado',
    'version': '1.0.10',
    'description': 'Pytest-bravado automatically generates from OpenAPI specification client fixtures.',
    'long_description': 'pytest-bravado\n==============\n\nPytest-bravado automatically generates client fixtures from OpenAPI specification.\n`Bravado documentation <https://github.com/Yelp/bravado>`__.\n\nInstallation\n-------------\n\nTo install pytest-bravado via pip run the following command:\n\n.. code-block:: bash\n\n    pip install pytest-bravado\n\nExample Usage\n-------------\n\n**Simple tests:**\n\n.. code-block:: Python\n\n    import pytest\n\n    @pytest.mark.parametrize(\'getUser\', [{\'id\': 1}], indirect=True)\n    def test_get_user(getUser):\n        assert getUser.result\n\n\n    @pytest.mark.parametrize(\'createUser\', [{\'id\': 2, \'username\': \'Ivan\'}], indirect=True)\n    def test_create_user(createUser, getUser):\n        assert getUser(id=2).response().result\n\n**Support openapi example:**\n\nIf there is an instance in the specifics, it will be used as the default request body.\n\n.. code-block:: yaml\n\n    parameters:\n      - in: "body"\n        name: "body"\n        schema:\n          $ref: "#/definitions/User"\n        example:\n          id: 10\n          username: Oleg\n\n.. code-block:: Python\n\n    import pytest\n\n    def test_create_user(createUser):\n        assert createUser.response().result\n\n*request body:*\n\n.. code-block:: Python\n\n    {\'id\': 10, \'username\': \'Oleg\'}\n\nYou can use mark parametrize to change all or part of the example.\n\n.. code-block:: Python\n\n    @pytest.mark.parametrize(\'createUser\', [{\'username\': \'Ivan\'}], indirect=True)\n    def test_create_user(createUser):\n        assert createUser.result\n\n*request body:*\n\n.. code-block:: Python\n\n    {\'id\': 10, \'username\': \'Ivan\'}\n\n**Run:**\n\n.. code-block:: bash\n\n    pytest --swagger_url http://user-service.com/swagger.json\n\n**Spec example:**\n\n.. code-block:: yaml\n\n    swagger: "2.0"\n    info:\n      version: "1.0.0"\n      title: "User service"\n    host: "user-service.com"\n    schemes:\n    - "http"\n    paths:\n      /user{id}:\n        get:\n          operationId: "getUser"\n          parameters:\n          - in: "path"\n            name: "id"\n            required: true\n            type: "integer"\n          responses:\n            default:\n              description: "successful"\n              schema:\n                $ref: "#/definitions/User"\n      /createUser:\n        post:\n          operationId: "createUser"\n          produces:\n          - "application/json"\n          parameters:\n          - in: "body"\n            name: "body"\n            schema:\n              $ref: "#/definitions/User"\n            example:\n              id: 10\n              username: Oleg\n          responses:\n            default:\n              description: "successful"\n    definitions:\n      User:\n        type: "object"\n        properties:\n          id:\n            type: "integer"\n          username:\n            type: "string"\n\nThe following flags are supported\n----------------------------------\n\n- `--swagger_url` - openapi spec url\n- `--request_headers` - request headers\n- `--not_validate_responses` - not validate incoming responses\n- `--not_validate_requests` - not validate outgoing requests\n- `--not_validate_swagger_spec` - not validate the swagger spec\n- `--not_use_models` - not use models (Python classes) instead of dicts for #/definitions/{models}\n- `--enable_fallback_results` - use fallback results even if they\'re provided\n- `--response_metadata_class` - What class to use for response metadata',
    'author': 'Viktor Kutepov',
    'author_email': 'vkytepov@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vkutepov/pytest-bravado',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
