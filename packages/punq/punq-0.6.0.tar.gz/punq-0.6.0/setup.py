# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['punq']

package_data = \
{'': ['*']}

install_requires = \
['expects>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'punq',
    'version': '0.6.0',
    'description': 'An IOC Container for Python 3.6+',
    'long_description': 'Punq\n====\n\n.. image:: https://codecov.io/gh/bobthemighty/punq/branch/master/graph/badge.svg?token=52hQhaggnk\n      :target: https://codecov.io/gh/bobthemighty/punq\n\n.. image:: https://readthedocs.org/projects/punq/badge/?version=latest\n      :target: https://punq.readthedocs.io/en/latest/?badge=latest\n      :alt: Documentation Status\n\nAn unintrusive library for dependency injection in modern Python.\nInspired by `Funq`_, Punq is a dependency injection library you can understand.\n\n- No global state\n- No decorators\n- No weird syntax applied to arguments\n- Small and simple code base with 100% test coverage and developer-friendly comments.\n\nInstallation\n------------\n\nPunq is available on the `cheese shop`_.\n\n.. code:: bash\n\n    pip install punq\n\nDocumentation is available on `Read the docs`_.\n\nQuick Start\n-----------\n\nPunq avoids global state, so you must explicitly create a container in the entrypoint of your application:\n\n.. code:: python\n\n   import punq\n\n   container = punq.Container()\n\nOnce you have a container, you can register your application\'s dependencies. In the simplest case, we can register any arbitrary object with some key:\n\n.. code:: python\n\n   container.register("connection_string", instance="postgresql://...")\n\nWe can then request that object back from the container:\n\n.. code:: python\n\n   conn_str = container.resolve("connection_string")\n\nUsually, though, we want to register some object that implements a useful service.:\n\n.. code:: python\n\n   class ConfigReader:\n      def get_config(self):\n         pass\n\n   class EnvironmentConfigReader(ConfigReader):\n      def get_config(self):\n         return {\n            "logging": {\n               "level": os.env.get("LOGGING_LEVEL", "debug")\n            },\n            "greeting": os.env.get("GREETING", "Hello world")\n         }\n\n   container.register(ConfigReader, EnvironmentConfigReader)\n\nNow we can `resolve` the `ConfigReader` service, and receive a concrete implementation:\n\n.. code:: python\n\n   config = container.resolve(ConfigReader).get_config()\n\nIf our application\'s dependencies have their *own* dependencies, Punq will inject those, too:\n\n.. code:: python\n\n   class Greeter:\n      def greet(self):\n         pass\n\n\n   class ConsoleGreeter(Greeter):\n      def __init__(self, config_reader: ConfigReader):\n         self.config = config_reader.get_config()\n\n      def greet(self):\n         print(self.config[\'greeting\'])\n\n\n   container.register(Greeter, ConsoleGreeter)\n   container.resolve(Greeter).greet()\n\nIf you just want to resolve an object without having any base class, that\'s okay:\n\n.. code:: python\n\n   class Greeter:\n      def __init__(self, config_reader: ConfigReader):\n         self.config = config_reader.get_config()\n\n      def greet(self):\n         print(self.config[\'greeting\'])\n\n   container.register(Greeter)\n   container.resolve(Greeter).greet()\n\nAnd if you need to have a singleton object for some reason, we can tell punq to register a specific instance of an object:\n\n.. code:: python\n\n   class FileWritingGreeter:\n      def __init__(self, path, greeting):\n         self.path = path\n         self.message = greeting\n         self.file = open(self.path, \'w\')\n\n      def greet(self):\n         self.file.write(self.message)\n\n\n   one_true_greeter = FileWritingGreeter("/tmp/greetings", "Hello world")\n   container.register(Greeter, instance=one_true_greeter)\n\n\nYou might not know all of your arguments at registration time, but you can provide them later:\n\n.. code:: python\n\n   container.register(Greeter, FileWritingGreeter)\n   greeter = container.resolve(Greeter, path="/tmp/foo", greeting="Hello world")\n\nConversely, you might want to provide arguments at registration time, without adding them to the container:\n\n.. code:: python\n\n   container.register(Greeter, FileWritingGreeter, path="/tmp/foo", greeting="Hello world")\n\nFuller documentation is available on `Read the docs`_.\n\nGithub workflows, nox configuration, and linting gratefully stolen from `Hypermodern Python`_\n\n.. _cheese shop: https://pypi.org/project/punq/\n.. _Read the docs: http://punq.readthedocs.io/en/latest/\n.. _Funq: https://github.com/jlyonsmith/Funq\n.. _Hypermodern Python: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n',
    'author': 'Bob Gregory',
    'author_email': 'bob@codefiend.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bobthemighty/punq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
