#!/usr/bin/env python3

# Copyright 2025 Google LLC
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
"""Create a reference list in Chronicle."""

import json
from typing import Optional, List

from common import chronicle_auth
from common import regions
from google.auth.transport import requests

CHRONICLE_API_BASE_URL = "https://chronicle.googleapis.com"


def create_reference_list(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    reference_list_id: str,
    entries: List[str],
    syntax_type: str = "REFERENCE_LIST_SYNTAX_TYPE_PLAIN_TEXT_STRING",
    scope_names: Optional[List[str]] = None,
    description: Optional[str] = None,
) -> dict:
  """Create a new reference list in Chronicle.

    Args:
        http_session: Authorized session for HTTP requests.
        proj_id: GCP project id or number to which the target instance belongs.
        proj_instance: Customer ID (uuid with dashes) for the instance.
        proj_region: region in which the target project is located.
        reference_list_id: ID to use for the new reference list.
        entries: List of values to add to the reference list.
        syntax_type: Type of entries in the list. One of:
            REFERENCE_LIST_SYNTAX_TYPE_UNSPECIFIED
            REFERENCE_LIST_SYNTAX_TYPE_PLAIN_TEXT_STRING
            REFERENCE_LIST_SYNTAX_TYPE_REGEX
            REFERENCE_LIST_SYNTAX_TYPE_CIDR
        scope_names: Optional list of scope names. Each scope name should be in format:
            "projects/{project}/locations/{location}/instances/{instance}/dataAccessScopes/{scope_name}"
        description: Optional description of the reference list.

    Returns:
        Dict containing the created reference list.

    Raises:
        requests.exceptions.HTTPError: HTTP request resulted in an error
            (response.status_code >= 400).
    """
  base_url_with_region = regions.url_always_prepend_region(
      CHRONICLE_API_BASE_URL, proj_region)
  instance = f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}"
  url = f"{base_url_with_region}/v1alpha/{instance}/referenceLists"

  body = {
      "reference_list_id": reference_list_id,
      "syntax_type": syntax_type,
      "entries": [{
          "value": entry
      } for entry in entries],
  }

  if description:
    body["description"] = description

  if scope_names:
    body["scope_info"] = {"reference_list_scope": {"scope_names": scope_names}}

  response = http_session.request(
      "POST",
      url,
      json=body,
  )
  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()
  return response.json()
