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
@click.option("-k", "--kind", required=True, help="Get records by kind")
@handle_cli_exceptions
@command_with_output("results")
def _click_command(state: State, kind: str):
    """Get records"""
    return get(state, kind)


def get(state: State, kind: str):
    """Get records

    Args:
        state (State): Global state
        kind (str): Kind of the schema
    """
    print("NOTE: storage get is still a work in progress")
    connection = CliOsduClient(state.config)
    # NOTE: there is a difference between records and query endpoints
    # url = "records/id"
    # url = "query/records?limit=10000&kind=osdu:wks:work-product-component--WellLog:1.0.0"
    # TODO: What do we want - a list of id's or the actual records? Perhaps move id list to 'storage list'
    if kind is not None:
        url = "query/records?kind=" + kind
        json = connection.cli_get_returning_json(CONFIG_STORAGE_URL, url)
        return json

    request_data = {}
    # if identifier is not None:
    #     request_data["query"] = f'id:("{identifier}")'
    request_data["records"] = [
        "opendes:work-product-component--WellLog:14667082fc7e4dceb17af802904069fb"
    ]
    json = connection.cli_post_returning_json(CONFIG_STORAGE_URL, "query/records", request_data)
    return json
