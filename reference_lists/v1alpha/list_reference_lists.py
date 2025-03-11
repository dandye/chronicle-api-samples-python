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
"""List reference lists in Chronicle."""

from typing import Optional

from common import regions
from google.auth.transport import requests

CHRONICLE_API_BASE_URL = "https://chronicle.googleapis.com"


def list_reference_lists(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
) -> dict:
  """List reference lists in Chronicle.

    Args:
        http_session: Authorized session for HTTP requests.
        proj_id: GCP project id or number to which the target instance belongs.
        proj_instance: Customer ID (uuid with dashes) for the instance.
        proj_region: region in which the target project is located.
        page_size: Optional maximum number of reference lists to return.
        page_token: Optional page token from a previous response for pagination.

    Returns:
        Dict containing the list of reference lists and next page token if any.

    Raises:
        requests.exceptions.HTTPError: HTTP request resulted in an error
            (response.status_code >= 400).
    """
  base_url_with_region = regions.url_always_prepend_region(
      CHRONICLE_API_BASE_URL, proj_region)
  instance = f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}"
  url = f"{base_url_with_region}/v1alpha/{instance}/referenceLists"

  params = []
  if page_size:
    params.append(f"pageSize={page_size}")
  if page_token:
    params.append(f"pageToken={page_token}")

  if params:
    url = f"{url}?{'&'.join(params)}"

  response = http_session.request("GET", url)
  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()
  return response.json()
