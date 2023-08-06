#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import asyncio
from typing import cast
from typing import TextIO

import click
from pydantic import AnyHttpUrl

from ra_flatfile_importer.models import MOFlatFileFormatImport
from ra_flatfile_importer.uploader import upload as mo_upload
from ra_flatfile_importer.util import model_validate_helper
from ra_flatfile_importer.util import takes_json_file
from ra_flatfile_importer.util import validate_url


def mo_validate_helper(json_file: TextIO) -> MOFlatFileFormatImport:
    return cast(
        MOFlatFileFormatImport, model_validate_helper(MOFlatFileFormatImport, json_file)
    )


@click.group(
    context_settings=dict(
        max_content_width=120,
    ),
)
def cli() -> None:
    """
    OS2mo Flatfile importer.

    Used to validate and load flatfile data (JSON) into OS2mo.
    """
    pass


@cli.command()
@takes_json_file
def validate(json_file: TextIO) -> None:
    """Validate the provided JSON file."""
    mo_validate_helper(json_file)


@cli.command()
@click.option(
    "--indent", help="Pass 'indent' to json serializer", type=click.INT, default=None
)
def schema(indent: int) -> None:
    """Generate JSON schema for valid files."""
    click.echo(MOFlatFileFormatImport.schema_json(indent=indent))


@cli.command()
@click.option(
    "--mo-url",
    help="OS2mo URL.",
    required=True,
    callback=validate_url,
    envvar="MO_URL",
    show_envvar=True,
)
@click.option(
    "--client-id",
    help="Client ID used to authenticate against OS2mo.",
    required=True,
    default="dipex",
    show_default=True,
    envvar="CLIENT_ID",
    show_envvar=True,
)
@click.option(
    "--client-secret",
    help="Client secret used to authenticate against OS2mo.",
    required=True,
    envvar="CLIENT_SECRET",
    show_envvar=True,
)
@click.option(
    "--auth-server",
    help="Keycloak authentication server.",
    required=True,
    callback=validate_url,
    envvar="AUTH_SERVER",
    show_envvar=True,
)
@click.option(
    "--auth-realm",
    help="Keycloak realm for OS2mo authentication.",
    default="mo",
    show_default=True,
    envvar="AUTH_REALM",
    show_envvar=True,
)
@takes_json_file
def upload(
    json_file: TextIO,
    mo_url: AnyHttpUrl,
    client_id: str,
    client_secret: str,
    auth_server: AnyHttpUrl,
    auth_realm: str,
) -> None:
    """Validate the provided JSON file and upload its contents."""
    flat_file_import = mo_validate_helper(json_file)
    asyncio.run(
        mo_upload(
            flat_file_import=flat_file_import,
            mo_url=mo_url,
            client_id=client_id,
            client_secret=client_secret,
            auth_server=auth_server,
            auth_realm=auth_realm,
        )
    )
