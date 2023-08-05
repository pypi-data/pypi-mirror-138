# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flexmock']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flexmock',
    'version': '0.11.3',
    'description': 'flexmock is a testing library for Python that makes it easy to create mocks, stubs and fakes.',
    'long_description': '<p align="center">\n  <img alt="banner" src="https://user-images.githubusercontent.com/25169984/138661460-969caf9e-8e88-4609-87c4-1a0ab9624ee4.png">\n</p>\n\n<p align="center"><strong>flexmock</strong> <em>- Mock, stub, and spy library for Python.</em></p>\n\n<p align="center">\n<a href="https://pypi.org/project/flexmock/">\n  <img src="https://img.shields.io/pypi/v/flexmock" alt="pypi">\n</a>\n<a href="https://github.com/flexmock/flexmock/actions/workflows/ci.yml">\n  <img src="https://github.com/flexmock/flexmock/actions/workflows/ci.yml/badge.svg" alt="ci">\n</a>\n<a href="https://flexmock.readthedocs.io/">\n  <img src="https://img.shields.io/readthedocs/flexmock" alt="documentation">\n</a>\n<a href="https://codecov.io/gh/flexmock/flexmock">\n  <img src="https://codecov.io/gh/flexmock/flexmock/branch/master/graph/badge.svg?token=wRgtiGxhiL" alt="codecov">\n</a>\n<a href="./LICENSE">\n  <img src="https://img.shields.io/pypi/l/flexmock" alt="license">\n</a>\n</p>\n\n---\n\nFlexmock is a testing library for Python that makes it easy to create mocks, stubs, and fakes.\n\n## Features\n\n- **Mock**: Easily create mock objects and make assertions about which methods or attributes were used and arguments they were called with.\n- **Spy**: Proxy calls to object\'s original methods or attributes and make assertions based on return values or call count.\n- **Fake**: Generate a fake objects to be used in your tests with ease.\n- **Stub**: Create stub objects which replace parts of existing objects and classes with just one call.\n- **No external dependencies**: Flexmock is lightweight and only uses Python standard library. There are no external dependencies.\n- **Simple and intuitive**: Declarations are structured to read more like English sentences than API calls, so they are easy to learn and use.\n- **Fully type annotated**: External API is fully type annotated so it works great with static analysis tools and editor auto-completion.\n- **Integrations with test runners**: Integrates seamlessly with all major test runners like unittest, doctest, and pytest.\n- **Python 3.6+ and PyPy3**: Extensively tested to work with latest Python versions.\n\n## Installation\n\nInstall with pip:\n\n```\npip install flexmock\n```\n\n## Examples\n\nFlexmock features smooth integration with pretty much every popular test runner, so no special setup is necessary. Simply importing flexmock into your test module is sufficient to get started with any of the following examples:\n\n```python\nfrom flexmock import flexmock\n```\n\n### Mocks\n\nAssertions take many flavors and flexmock has many different facilities to generate them:\n\n```python\n# Simplest is ensuring that a certain method is called\nflexmock(Train).should_receive("get_tickets").once()\n\n# Of course, it is also possible to provide a default return value\nflexmock(Train).should_receive("get_destination").and_return("Paris").once()\n\n# Or check that a method is called with specific arguments\nflexmock(Train).should_receive("set_destination").with_args("Seoul").at_least().twice()\n```\n\n### Spies\n\nInstead of mocking, there are also times when you want to execute the actual method and simply find out how many times it was called. Flexmock uses `should_call` to generate this sort of assertions instead of `should_receive`:\n\n```python\n# Verify that a method is called at most three times\nflexmock(Train).should_call("get_tickets").at_most().times(3)\n\n# Make sure that a method is never called with specific arguments\nflexmock(Train).should_call("set_destination").with_args("Helsinki").never()\n\n# More complex example with features like argument type and exception matching\nflexmock(Train).should_call("crash").with_args(str, int).and_raise(AttributeError).once()\n```\n\nSee more examples in the documentation.\n\n## Documentation\n\nUser guide, examples, and a full API reference is available at: https://flexmock.readthedocs.io\n\n## Contributing\n\nContributions are absolutely welcome and encouraged! See [CONTRIBUTING.md](https://github.com/flexmock/flexmock/blob/master/CONTRIBUTING.md) to get started.\n',
    'author': 'Slavek Kabrda',
    'author_email': None,
    'maintainer': 'Adarsh Krishnan',
    'maintainer_email': 'adarshk7@gmail.com',
    'url': 'https://github.com/flexmock/flexmock',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
