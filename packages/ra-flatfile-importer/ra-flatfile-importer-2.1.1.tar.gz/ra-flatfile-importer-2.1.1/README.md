<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->


# RA Flatfile importer


## Usage
The primary usage of this tool is to validate and load flatfile data (JSON) into OS2mo, for example fixtures generated
using [ra-flatfile-importer](https://git.magenta.dk/rammearkitektur/ra-fixture-generator).
```
Usage: python -m ra_flatfile_importer [OPTIONS] COMMAND [ARGS]...

  OS2mo Flatfile importer.

  Used to validate and load flatfile data (JSON) into OS2mo.

Options:
  --help  Show this message and exit.

Commands:
  schema    Generate JSON schema for valid files.
  upload    Validate the provided JSON file and upload its contents.
  validate  Validate the provided JSON file.
```

On a development machine with the OS2mo stack running, the following will upload a previously-generated flatfile:
```
python -m ra_flatfile_importer upload \
  --mo-url=http://localhost:5000 \
  --client-secret=603f1c82-d012-4d04-9382-dbe659c533fb \
  --auth-server=http://localhost:8081/auth \
  --json-file=mo.json
```

The tool has various other commands too, such as producing the validation schema for the flat file format:
```
python -m ra_flatfile_importer schema --indent=4
```
Which yields:
```
{
    "title": "MOFlatFileFormatImport",
    "description": "Flatfile format for OS2mo.\n\nEach chunk in the list is send as bulk / in parallel, and as such 
                    entries\nwithin a single chunk should not depend on other entries within the same chunk.\n\nMinimal 
                    valid example is [].",
    "type": "object",
    "properties": {
        "chunks": {
            ...
        },
        ...
    }
}
```

Or for validating whether a file is invalid:
```
python -m ra_flatfile_importer validate < mo.json
```


## Versioning
This project uses [Semantic Versioning](https://semver.org/) with the following strategy:
- MAJOR: Incompatible changes to existing commandline interface
- MINOR: Backwards compatible updates to commandline interface
- PATCH: Backwards compatible bug fixes

The fileformat is versioned directly, and the version is exported in the file itself.


## License
- This project: [MPL-2.0](LICENSES/MPL-2.0.txt)
- Dependencies:
  - pydantic: [MIT](LICENSES/MIT.txt)

This project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
