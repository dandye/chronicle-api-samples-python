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
r"""Executable and reusable sample for ingesting events in UDM format.

WARNING: This script makes use of the Ingestion API v1alpha. v1alpha is currently only in
preview for certain Chronicle customers. Please reach out to your Chronicle
representative if you wish to use this API.

The Unified Data Model (UDM) is a way of representing events across all log
sources. See
https://cloud.google.com/chronicle/docs/unified-data-model/udm-field-list for a
description of UDM fields, and see
https://cloud.google.com/chronicle/docs/unified-data-model/format-events-as-udm
for how to describe a log as an event in UDM format.

This command accepts a path to a file (--json_events_file) that contains an
array of JSON formatted events in UDM format. See
./example_input/sample_udm_events.json for an example.

So, assuming you've created a credentials file at $HOME/.chronicle_credentials.json,
and you are using environment variables for your PROJECT_GUID and PROJECT_ID,
you can run this command using the sample input like so:

$ python3 -m ingestion.v1alpha.create_udm_events \
  --project_guid $PROJECT_GUID \
  --project_id $PROJECT_ID \
  --json_events_file=./ingestion/example_input/sample_udm_events.json

API reference:
https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.events/import
https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.events/import#EventsInlineSource
https://cloud.google.com/chronicle/docs/reference/udm-field-list
https://cloud.google.com/chronicle/docs/unified-data-model/udm-usage
"""

import argparse
import json

from google.auth.transport import requests
from google.oauth2 import service_account

from common import (
  chronicle_auth,
  project_guid,
  project_id,
  regions,
)

INGESTION_API_BASE_URL = "https://malachiteingestion-pa.googleapis.com"
AUTHORIZATION_SCOPES = ["https://www.googleapis.com/auth/malachite-ingestion"]

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
]


def authorize(credentials_file_path, scopes):
    """
    Obtains an authorized session using the provided credentials.

    Args:
        credentials (google.oauth2.service_account.Credentials): The service account credentials.

    Returns:
        requests.AuthorizedSession: An authorized session for making API calls.
    """
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file_path, scopes=scopes
    )
    return requests.AuthorizedSession(credentials)


def create_udm_events(http_session: requests.AuthorizedSession, json_events: str) -> None:
  """Sends a collection of UDM events to the Chronicle backend for ingestion.

  A Unified Data Model (UDM) event is a structured representation of an event
  regardless of the log source.

  Args:
    http_session: Authorized session for HTTP requests.
    customer_id: A string containing the UUID for the Chronicle customer.
    json_events: A collection of UDM events in (serialized) JSON format.

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).

  Requires the following IAM permission on the parent resource:
  chronicle.events.import

  POST https://chronicle.googleapis.com/v1alpha/{parent}/events:import

  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.events/import
  """
  url = f"{INGESTION_API_BASE_URL}/v2/udmevents:batchCreate"

  parent = f"projects/{args.project_id}/locations/{args.region}/instances/{args.project_guid}"
  url = f"https://{args.region}-chronicle.googleapis.com/v1alpha/{parent}/events:import"

  body = {
    "inline_source": {
      "events": [
        {
          "name": "foo",
          "udm": json.loads(json_events)[0],
        }
      ]
    }
  }

  response = http_session.request("POST", url, json=body)
  if response.status_code >= 400:
        print(body)
        print(response.text)
  response.raise_for_status()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  # common
  chronicle_auth.add_argument_credentials_file(parser)
  project_guid.add_argument_project_guid(parser)
  project_id.add_argument_project_id(parser)
  regions.add_argument_region(parser)
  # local
  parser.add_argument(
      "--json_events_file",
      type=argparse.FileType("r"),
      required=True,
      help="path to a file (or \"-\" for STDIN) containing a list of UDM "
      "events in json format")
  args = parser.parse_args()

  auth_session = authorize(args.credentials_file, SCOPES)
  create_udm_events(auth_session, args.json_events_file.read())
