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

"""Schema service get command"""

import click

from osducli.click_cli import CustomClickCommand, State, command_with_output
from osducli.cliclient import CliOsduClient, handle_cli_exceptions
from osducli.config import CONFIG_STORAGE_URL


# click entry point
@click.command(cls=CustomClickCommand)
@click.option("-k", "--kind", help="Get records by kind")
@click.option("-id", "--id", "_id", help="An id to search for")
@handle_cli_exceptions
@command_with_output("records || results")
def _click_command(state: State, kind: str, _id: str):
    """Get records"""
    return get(state, kind, _id)


def get(
    state: State, kind: str = None, id: str = None
):  # pylint: disable=invalid-name,redefined-builtin
    """Get records

    Args:
        state (State): Global state
        kind (str): Kind of records
        id (str): Id of records
    """
    print("NOTE: storage get is still a work in progress and subject to change")
    connection = CliOsduClient(state.config)

    # NOTE: there is a difference between records and query endpoints
    # url = "records/id"
    # url = "query/records?limit=10000&kind=osdu:wks:work-product-component--WellLog:1.0.0"

    if kind is not None:
        print("Work in progress - needs to query individual records")
        url = "query/records?kind=" + kind
        json = connection.cli_get_returning_json(CONFIG_STORAGE_URL, url)
        return json

    if id is not None:
        request_data = {}
        # if identifier is not None:
        #     request_data["query"] = f'id:("{identifier}")'
        request_data["records"] = [id]
        json = connection.cli_post_returning_json(CONFIG_STORAGE_URL, "query/records", request_data)
        return json

    raise ValueError("You must specify either a kind or id")
