# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma',
 'sigma.backends.test',
 'sigma.conversion',
 'sigma.pipelines',
 'sigma.processing',
 'sigma.tools']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=2.4.7,<3.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['sigma-converter = sigma.tools.converter:main']}

setup_kwargs = {
    'name': 'pysigma',
    'version': '0.1.7',
    'description': 'Sigma rule processing and conversion tools',
    'long_description': "# pySigma\n\n![Tests](https://github.com/SigmaHQ/pySigma/actions/workflows/test.yml/badge.svg)\n![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/thomaspatzke/11b31b4f709b6dc54a30d5203e8fe0ee/raw/SigmaHQ-pySigma-coverage.json)\n![Status](https://img.shields.io/badge/Status-pre--release-orange)\n\n`pySigma` is a python library that parses and converts Sigma rules into queries.\n\nIt replaces a lot of the logic found in the `sigmac` tool, and brings it into a modern Python library. For a CLI version of the new Sigma tool, see (TBA).\n\n## Getting Started\n\nTo start using `pySigma`, install it using your python package manager of choice. Documentation with\nsome usage examples can be found [here](https://sigmahq-pysigma.readthedocs.io/).\n\n**Poetry:**\n\n```bash\npoetry add git+https://github.com/SigmaHQ/pySigma.git#main\n```\n\n**Pipenv:**\n\n```bash\npipenv install git+https://github.com/SigmaHQ/pySigma.git#egg=pysigma\n```\n\n## Features\n\n`pySigma` brings a number of additional features over `sigmac`, as well as some changes.\n\n### Modifier compare from sigmac\n\n|Modifier|Use|sigmac legacy|\n|--------|---|:-------------:|\n|contains|the value is matched anywhere in the field (strings and regular expressions)|X|\n|startswith|The value is expected at the beginning of the field's content (strings and regular expressions)|X|\n|endswith|The value is expected at the end of the field's content (strings and regular expressions)|X|\n|base64|The value is encoded with Base64|X|\n|base64offset|If a value might appear somewhere in a base64-encoded value the representation might change depending on the position in the overall value|X|\n|wide|transforms value to UTF16-LE encoding|X|\n|re|value is handled as regular expression by backends|X|\n|cidr|value is handled as a IP CIDR by backends||\n|all|This modifier changes OR logic to AND|X|\n|lt|Field is less than the value||\n|lte|Field is less or egal than the value||\n|gt|Field is Greater than the value||\n|gte|Field is Greater or egal than the value||\n|expand|Modifier for expansion of placeholders in values. It replaces placeholder strings (%something%)||\n\n## Overview\n\nConversion Overview\n\n![Conversion Graph](/docs/images/conversion.png)\n\nPipelines\n\n![Conversion Graph](/docs/images/pipelines.png)\n\nMore details are described in [the documentation](https://sigmahq-pysigma.readthedocs.io/).\n\n## Testing\n\nTo run the pytest suite for `pySigma`, run the following command:\n\n```bash\nmake test\n```\n\n## Contributing\n\nPull requests are welcome. Please feel free to lodge any issues/PRs as discussion points.\n\n## Authors\n\n- Thomas Patzke <thomas@patzke.org>\n\n## Licence\n\nGNU Lesser General Public License v2.1. For details, please see the full license file [located here](https://github.com/SigmaHQ/pySigma/blob/main/LICENSE).\n",
    'author': 'Thomas Patzke',
    'author_email': 'thomas@patzke.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SigmaHQ/pySigma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
