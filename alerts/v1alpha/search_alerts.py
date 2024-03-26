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
r"""Executable and reusable sample for getting Alerts.

Usage:
  python -m alerts.v1alpha.get_alert \
    --project_id=<PROJECT_ID>   \
    --project_instance=<PROJECT_INSTANCE> \
    --start_time=<START_TIME; yyyy-mm-ddThh:mm:ssZ" or "yyyy-mm-ddThh:mm:ss.sssssssssZ"
    --end_time=<END_TIME> \
    --end_time=<END_TIME> \
    --page_size=<PAGE_SIZE> \
    --page_token=<PAGE_TOKEN>

API reference:
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.legacy/legacySearchAlerts

"""

import argparse
import json
from typing import Any, Mapping

from common import chronicle_auth
from common import project_id
from common import project_instance
from common import regions

from google.auth.transport import requests

ALERT_RESPONSE_MODE_ENUM = (
    "ALERT_RESPONSE_MODE_UNSPECIFIED",
    "INCLUDE_RAW_LOG",
    "EVENT_ONLY"
)
CHRONICLE_API_BASE_URL = "https://chronicle.googleapis.com"
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
]


def search_alerts(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    start_time: str,
    end_time: str,
    page_size: int,
    page_token: str,
    alert_response_mode: str,
) -> Mapping[str, Any]:
  """Search Alerts.

  Args:
    http_session: Authorized session for HTTP requests.
    proj_id: GCP project id or number to which the target instance belongs.
    proj_instance: Customer ID (uuid with dashes) for the Chronicle instance.
    proj_region: region in which the target project is located.
    start_time: Start of time range, inclusive, to search for alerts.
    end_time: End of time range, exclusive, to search for alerts.
    page_size: Number of Alerts to return.
    page_token: Page token from a previous request.
    alert_response_mode: Retrieve the full raw log associated with each event.

  Returns:
    Dictionary representation of the Alerts
  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).
  """
  base_url_with_region = regions.url_always_prepend_region(
      CHRONICLE_API_BASE_URL,
      proj_region
  )
  # pylint: disable-next=line-too-long
  parent = f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}"
  # required
  query_params = f"?startTime={start_time}&endTime={end_time}"
  # optional
  if page_size:
    query_params += f"&pageSize={page_size}"
  if page_token:
    query_params += f"&pageToken={page_token}"
  if alert_response_mode:
    query_params += f"&alertResponseMode={alert_response_mode}"

  # pylint: disable-next=line-too-long
  url = f"{base_url_with_region}/v1alpha/{parent}/legacy:legacySearchAlerts{query_params}"
  response = http_session.request("GET", url)
  # Expected server response is described in:
  # https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.legacy/legacyGetAlert
  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()
  return response.json()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  chronicle_auth.add_argument_credentials_file(parser)
  project_instance.add_argument_project_instance(parser)
  project_id.add_argument_project_id(parser)
  regions.add_argument_region(parser)
  parser.add_argument(
      "--start_time", type=str, required=True,
      help="start time for the query"
  )
  parser.add_argument(
      "--end_time", type=str, required=True,
      help="end time for the query"
  )
  parser.add_argument(
      "--page_size", type=int, required=False,
      default=10,
      help="number of alerts to return"
  )
  parser.add_argument(
      "--page_token", type=str, required=False,
      help="page token from a previous request"
  )
  parser.add_argument(
      "--alert_response_mode", choices=ALERT_RESPONSE_MODE_ENUM,
      required=False, default=ALERT_RESPONSE_MODE_ENUM[0],
      help="response mode"
  )

  args = parser.parse_args()

  auth_session = chronicle_auth.initialize_http_session(
      args.credentials_file,
      SCOPES,
  )
  alert = search_alerts(
      auth_session,
      args.project_id,
      args.project_instance,
      args.region,
      args.start_time,
      args.end_time,
      args.page_size,
      args.page_token,
      args.alert_response_mode,
  )
  print(json.dumps(alert, indent=2))
