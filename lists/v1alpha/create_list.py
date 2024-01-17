#!/usr/bin/env python3

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Executable and reusable sample for creating a Reference List."""

import argparse
from typing import Sequence

from google.auth.transport import requests
from google.oauth2 import service_account

from common import chronicle_auth
from common import regions

SCOPES = ['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/chronicle-backstory']


def authorize(credentials_file_path, scopes):
    """
    Obtains an authorized session using the provided credentials.

    Args:
        credentials (google.oauth2.service_account.Credentials): The service account credentials.

    Returns:
        requests.AuthorizedSession: An authorized session for making API calls.
    """
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=scopes)
    return requests.AuthorizedSession(credentials)


def create_list(http_session: requests.AuthorizedSession,
                name: str,
                description: str,
                content_lines: Sequence[str],
                content_type: str) -> str:
    """Creates a list.

    Args:
      http_session: Authorized session for HTTP requests.
      name: Unique name for the list.
      description: Description of the list.
      content_lines: Array containing each line of the list's content.
      content_type: Type of list content, indicating how to interpret this list.

    Returns:
      Creation timestamp of the new list.

    Raises:
      requests.exceptions.HTTPError: HTTP request resulted in an error
        (response.status_code >= 400).
    """

    parent=f"projects/{args.project_id}/locations/{args.region}/instances/{args.project_guid}"
    url = f"https://{args.region}-chronicle.googleapis.com/v1alpha/{parent}/referenceLists"
    # Test auth
    response = http_session.request("GET", url)
    if response.status_code >= 400:
        print(response.text)
    response.raise_for_status()
    entries = []
    for content_line in content_lines:
        entries.append({"value": content_line.strip()})

    body = {
        "name": name,
        "description": description,
        "entries": entries,
        "syntax_type": content_type,
    }
    url_w_query_string = f"{url}?referenceListId={name}"
    response = http_session.request("POST", url_w_query_string, json=body)
    # Expected server response:
    # response.json().keys()
    # dict_keys(['name', 'displayName', 'revisionCreateTime', 'description', 'entries', 'syntaxType'])
    if response.status_code >= 400:
        print(response.text)
    response.raise_for_status()
    return response.json()["revisionCreateTime"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    chronicle_auth.add_argument_credentials_file(parser)
    regions.add_argument_region(parser)
    parser.add_argument(
        "-n", "--name", type=str, required=True, help="unique name for the list")
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        required=True,
        help="description of the list")
    parser.add_argument(
        "-t",
        "--syntax_type",
        type=str,
        default="REFERENCE_LIST_SYNTAX_TYPE_PLAIN_TEXT_STRING",
        help="type of list lines")
    parser.add_argument(
        "-f",
        "--list_file",
        type=argparse.FileType("r"),
        required=True,
        # File example:
        #   python3 -m lists.create_list <other args> -f <path>
        # STDIN example:
        #   cat <path> | python3 -m lists.create_list <other args> -f -
        help="path of a file containing the list content, or - for STDIN")
    parser.add_argument(
        "-p",
        "--project_id",
        type=str,
        required=True,
        help="Your BYOP, project id")
    parser.add_argument(
        "-g",
        "--project_guid",
        type=str,
        required=True,
        help="Your Chronicle instance's GUID")

    args = parser.parse_args()
    auth_session = authorize(args.credentials_file, SCOPES)
    new_list_create_time = create_list(auth_session, args.name, args.description,
                                        args.list_file.read().splitlines(),
                                        args.syntax_type,
                                        )
    print(f"New list created successfully, at {new_list_create_time}")
