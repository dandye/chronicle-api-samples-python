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
# pylint: disable=line-too-long
r"""Executable and reusable v1alpha API sample for creating a Reference List.

Usage:
  python -m lists.v1alpha.create_list \
    --project_id=<PROJECT_ID> \
    --project_instance=<PROJECT_INSTANCE> \
    --region=<REGION> \
    --name=<LIST_NAME> \
    --description=<LIST_DESCRIPTION> \
    --list_file=<PATH_TO_LIST_FILE>

API reference:
https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.referenceLists/create
"""
# pylint: enable=line-too-long

import argparse
import json
from typing import Any, Dict, Optional, Sequence

from google.auth.transport import requests

from common import chronicle_auth
from common import project_id
from common import project_instance
from common import regions

CHRONICLE_API_BASE_URL = "https://chronicle.googleapis.com"
SCOPES = [
  "https://www.googleapis.com/auth/cloud-platform",
]

PREFIX = "REFERENCE_LIST_SYNTAX_TYPE_"
SYNTAX_TYPE_ENUM = [
  f"{PREFIX}UNSPECIFIED",  # Defaults to ..._PLAIN_TEXT_STRING.
  f"{PREFIX}PLAIN_TEXT_STRING",  # List contains plain text patterns.
  f"{PREFIX}REGEX",  # List contains only Regular Expression patterns.
  f"{PREFIX}CIDR",  # List contains only CIDR patterns.
]


def create_list(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    name: str,
    description: str,
    content_lines: Sequence[str],
    content_type: str,
    scope_name: Optional[str] | None = None,
) -> Dict[str, Any]:
  """Creates a reference list using the Create Reference List API.

  Args:
    http_session: Authorized session for HTTP requests.
    proj_id: GCP project id or number to which the target instance belongs.
    proj_instance: Customer ID (uuid with dashes) for the Chronicle instance.
    proj_region: region in which the target project is located.
    name: Unique name for the list.
    description: Description of the list.
    content_lines: Array containing each line of the list's content.
    content_type: Type of list content, indicating how to interpret this list.
    scope_name: (Optional) Data RBAC scope name for the list.

  Returns:
    Dictionary representation of the created Reference List.

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).

  Requires the following IAM permission on the parent resource:
  chronicle.referenceLists.create
  """
  base_url_with_region = regions.url_always_prepend_region(
      CHRONICLE_API_BASE_URL,
      proj_region
  )
  parent = f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}"
  url = f"{base_url_with_region}/v1alpha/{parent}/referenceLists"

  # Create entries in format [{"value": <string>}, ...]
  entries = [{"value": line.strip()} for line in content_lines]

  body = {
      "name": name,
      "description": description,
      "entries": entries,
      "syntax_type": content_type,
  }

  if scope_name:
    body["scope_info"] = {
        "referenceListScope": {
            "scopeNames": [
                f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}/dataAccessScopes/{scope_name}"
            ]
        }
    }
  else:
    body["scope_info"] = None

  params = {"referenceListId": name}
  response = http_session.request("POST", url, params=params, json=body)
  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()
  
  return response.json()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  # common
  chronicle_auth.add_argument_credentials_file(parser)
  project_instance.add_argument_project_instance(parser)
  project_id.add_argument_project_id(parser)
  regions.add_argument_region(parser)
  # local
  parser.add_argument(
      "--name",
      type=str,
      required=True,
      help="Unique name for the list"
  )
  parser.add_argument(
      "--description",
      type=str,
      required=True,
      help="Description of the list"
  )
  parser.add_argument(
      "--scope_name",
      type=str,
      help="Data RBAC scope name for the list"
  )
  parser.add_argument(
      "--syntax_type",
      type=str,
      required=False,
      default="REFERENCE_LIST_SYNTAX_TYPE_PLAIN_TEXT_STRING",
      choices=SYNTAX_TYPE_ENUM,
      help="Syntax type of the list, used for validation"
  )
  parser.add_argument(
      "--list_file",
      type=argparse.FileType("r"),
      required=True,
      help="Path to file containing list content, or - for STDIN"
  )

  args = parser.parse_args()

  auth_session = chronicle_auth.initialize_http_session(
      args.credentials_file,
      SCOPES
  )
  result = create_list(
      auth_session,
      args.project_id,
      args.project_instance,
      args.region,
      args.name,
      args.description,
      args.list_file.read().splitlines(),
      args.syntax_type,
      args.scope_name,
  )
  print(json.dumps(result, indent=2))
