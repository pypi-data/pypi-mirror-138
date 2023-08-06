#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Version command"""

import json

import click

from osducli.click_cli import CustomClickCommand, State, command_with_output
from osducli.cliclient import CliOsduClient, handle_cli_exceptions
from osducli.config import CONFIG_STORAGE_URL
from osducli.log import get_logger
from osducli.util.file import get_files_from_path

logger = get_logger(__name__)


# click entry point
@click.command(cls=CustomClickCommand)
@click.option(
    "-p",
    "--path",
    help="Path to a record or records to add.",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, resolve_path=True),
    required=True,
)
@click.option(
    "-b",
    "--batch",
    help="Number of records to add per API call. If not specified records are uploaded as is.",
    is_flag=False,
    flag_value=200,
    type=int,
    default=None,
    show_default=True,
)
@handle_cli_exceptions
@command_with_output(None)
def _click_command(state: State, path: str, batch: int):
    """Add or update a record"""
    return add_records(state, path, batch)


# pylint: disable=too-many-locals
def add_records(state: State, path: str, batch: int) -> dict:
    """Add or update a record

    Args:
        state (State): Global state
        path (str): Path to a record or records to add.
        batch (int): Batch size per API call. If None then ingest as is
    Returns:
        dict: Response from service
    """
    if batch is not None:
        raise NotImplementedError("--batch is not supported yet for storage add")

    connection = CliOsduClient(state.config)

    files = get_files_from_path(path)
    logger.debug("Files list: %s", files)

    # TODO: Check if loaded file is already an array, or a single file
    # TODO: Batch uploads
    responses = []
    for filepath in files:
        if filepath.endswith(".json"):
            with open(filepath) as file:
                storage_object = json.load(file)

                logger.info("Processing file %s.", filepath)
                if isinstance(storage_object, list):
                    payload = storage_object
                else:
                    payload = [storage_object]

                response_json = None
                response_json = connection.cli_put_returning_json(
                    CONFIG_STORAGE_URL, "records", payload, [200, 201]
                )
                responses.append(response_json)
    return responses
