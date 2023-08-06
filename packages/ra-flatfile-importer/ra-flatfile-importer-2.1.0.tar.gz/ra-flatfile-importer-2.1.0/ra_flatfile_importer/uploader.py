#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from pydantic import AnyHttpUrl
from raclients.modelclient.mo import ModelClient
from tqdm import tqdm

from ra_flatfile_importer.models import concat_chunk
from ra_flatfile_importer.models import MOFlatFileFormatImport


async def upload(
    flat_file_import: MOFlatFileFormatImport,
    mo_url: AnyHttpUrl,
    client_id: str,
    client_secret: str,
    auth_server: AnyHttpUrl,
    auth_realm: str,
) -> None:
    async with ModelClient(
        base_url=mo_url,
        client_id=client_id,
        client_secret=client_secret,
        auth_server=auth_server,
        auth_realm=auth_realm,
    ) as client:
        tasks = (
            (flat_file_import.chunks, client.upload),
            (flat_file_import.edits, client.edit),
        )
        for chunks, send in tasks:
            for chunk in tqdm(chunks, desc="File chunks", unit="chunk"):
                objs = list(concat_chunk(chunk))
                if objs:
                    await send(objs)
