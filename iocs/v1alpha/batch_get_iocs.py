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
"""Get multiple IoCs from Chronicle."""

from typing import List, Mapping, Any

from common import regions
from google.auth.transport import requests

CHRONICLE_API_BASE_URL = "https://chronicle.googleapis.com"


def batch_get_iocs(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    ioc_values: List[str],
    ioc_type: str,
) -> Mapping[str, Any]:
  """Get multiple IoCs by their values from Chronicle.

  Args:
    http_session: Authorized session for HTTP requests.
    proj_id: GCP project id or number to which the target instance belongs.
    proj_instance: Customer ID (uuid with dashes) for the instance.
    proj_region: region in which the target project is located.
    ioc_values: List of IoC values to retrieve.
    ioc_type: Type of IoCs being requested. One of:
      IOC_TYPE_UNSPECIFIED
      DOMAIN
      IP
      FILE_HASH
      URL
      USER_EMAIL
      MUTEX
      FILE_HASH_MD5
      FILE_HASH_SHA1
      FILE_HASH_SHA256
      IOC_TYPE_RESOURCE

  Returns:
    Dict containing the requested IoCs.

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
        (response.status_code >= 400).
  """
  base_url_with_region = regions.url_always_prepend_region(
      CHRONICLE_API_BASE_URL, proj_region)
  instance = f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}"
  url = f"{base_url_with_region}/v1alpha/{instance}/iocs:batchGet"

  body = {
      "ioc_values": ioc_values,
      "ioc_type": ioc_type,
  }

  response = http_session.request(
      "POST",
      url,
      json=body,
  )
  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()
  return response.json()
