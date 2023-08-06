# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ra_flatfile_importer']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'ra-utils>=0.4.0,<0.5.0',
 'raclients>=1.2.1,<2.0.0',
 'ramodels>=5.3.2,<6.0.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'ra-flatfile-importer',
    'version': '2.1.1',
    'description': 'Flatfile importer for OS2mo',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>\nSPDX-License-Identifier: MPL-2.0\n-->\n\n\n# RA Flatfile importer\n\n\n## Usage\nThe primary usage of this tool is to validate and load flatfile data (JSON) into OS2mo, for example fixtures generated\nusing [ra-flatfile-importer](https://git.magenta.dk/rammearkitektur/ra-fixture-generator).\n```\nUsage: python -m ra_flatfile_importer [OPTIONS] COMMAND [ARGS]...\n\n  OS2mo Flatfile importer.\n\n  Used to validate and load flatfile data (JSON) into OS2mo.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  schema    Generate JSON schema for valid files.\n  upload    Validate the provided JSON file and upload its contents.\n  validate  Validate the provided JSON file.\n```\n\nOn a development machine with the OS2mo stack running, the following will upload a previously-generated flatfile:\n```\npython -m ra_flatfile_importer upload \\\n  --mo-url=http://localhost:5000 \\\n  --client-secret=603f1c82-d012-4d04-9382-dbe659c533fb \\\n  --auth-server=http://localhost:8081/auth \\\n  --json-file=mo.json\n```\n\nThe tool has various other commands too, such as producing the validation schema for the flat file format:\n```\npython -m ra_flatfile_importer schema --indent=4\n```\nWhich yields:\n```\n{\n    "title": "MOFlatFileFormatImport",\n    "description": "Flatfile format for OS2mo.\\n\\nEach chunk in the list is send as bulk / in parallel, and as such \n                    entries\\nwithin a single chunk should not depend on other entries within the same chunk.\\n\\nMinimal \n                    valid example is [].",\n    "type": "object",\n    "properties": {\n        "chunks": {\n            ...\n        },\n        ...\n    }\n}\n```\n\nOr for validating whether a file is invalid:\n```\npython -m ra_flatfile_importer validate < mo.json\n```\n\n\n## Versioning\nThis project uses [Semantic Versioning](https://semver.org/) with the following strategy:\n- MAJOR: Incompatible changes to existing commandline interface\n- MINOR: Backwards compatible updates to commandline interface\n- PATCH: Backwards compatible bug fixes\n\nThe fileformat is versioned directly, and the version is exported in the file itself.\n\n\n## License\n- This project: [MPL-2.0](LICENSES/MPL-2.0.txt)\n- Dependencies:\n  - pydantic: [MIT](LICENSES/MIT.txt)\n\nThis project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.\n',
    'author': 'Magenta',
    'author_email': 'info@magenta.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://magenta.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
