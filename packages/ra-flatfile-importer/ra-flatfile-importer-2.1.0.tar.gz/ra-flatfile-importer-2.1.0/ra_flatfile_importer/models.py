#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections.abc import Iterator
from itertools import chain
from typing import Any
from typing import Optional

from pydantic import validator
from ra_utils.semantic_version_type import SemanticVersion
from ramodels.mo import Employee
from ramodels.mo import MOBase
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Address
from ramodels.mo.details import Association
from ramodels.mo.details import Engagement
from ramodels.mo.details import ITUser
from ramodels.mo.details import KLEWrite
from ramodels.mo.details import Leave
from ramodels.mo.details import Manager
from ramodels.mo.details import Role

from ra_flatfile_importer.util import FrozenBaseModel

__mo_fileformat_version__: SemanticVersion = SemanticVersion("0.3.0")
__supported_mo_fileformat_versions__: list[SemanticVersion] = list(
    map(SemanticVersion, ["0.1.1", "0.2.0", "0.3.0"])
)
assert (
    __mo_fileformat_version__ in __supported_mo_fileformat_versions__
), "Generated MO version not supported"


class MOFlatFileFormatChunk(FrozenBaseModel):
    """Flatfile chunk for OS2mo.

    Each chunk in the list is send as bulk / in parallel, and as such entries
    within a single chunk should not depend on other entries within the same chunk.

    Minimal valid example is {}.
    """

    org_units: Optional[list[OrganisationUnit]]
    employees: Optional[list[Employee]]
    engagements: Optional[list[Engagement]]
    address: Optional[list[Address]]
    manager: Optional[list[Manager]]
    associations: Optional[list[Association]]
    roles: Optional[list[Role]]
    leaves: Optional[list[Leave]]
    it_users: Optional[list[ITUser]]
    kles: Optional[list[KLEWrite]]


class MOFlatFileFormatImport(FrozenBaseModel):
    """Flatfile format for OS2mo.

    Each chunk in the list is send as bulk / in parallel, and as such entries
    within a single chunk should not depend on other entries within the same chunk.

    Minimal valid example is [].
    """

    chunks: list[MOFlatFileFormatChunk]
    edits: list[MOFlatFileFormatChunk]
    version: SemanticVersion

    @validator("version", pre=True, always=True)
    def check_version(cls, v: Any) -> Any:
        if v not in __supported_mo_fileformat_versions__:
            raise ValueError("fileformat version not supported")
        return v


class MOFlatFileFormat(MOFlatFileFormatImport):
    """Flatfile format for OS2mo.

    Each chunk in the list is send as bulk / in parallel, and as such entries
    within a single chunk should not depend on other entries within the same chunk.

    Minimal valid example is [].
    """

    version: SemanticVersion = __mo_fileformat_version__


def concat_chunk(chunk: MOFlatFileFormatChunk) -> Iterator[MOBase]:
    """Convert a chunk to an iterator of objects."""
    return chain(
        chunk.org_units or [],
        chunk.employees or [],
        chunk.engagements or [],
        chunk.address or [],
        chunk.manager or [],
        chunk.associations or [],
        chunk.roles or [],
        chunk.leaves or [],
        chunk.it_users or [],
        chunk.kles or [],
    )
