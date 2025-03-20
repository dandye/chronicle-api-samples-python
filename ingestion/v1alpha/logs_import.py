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
#
"""API Sample to import logs."""
import argparse
import base64
import datetime
import json
import logging
from typing import Mapping, Any

from common import chronicle_auth
from common import project_instance
from common import project_id
from common import regions
from google.auth.transport import requests

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
]


def logs_import(
    http_session: requests.AuthorizedSession,
    logs_file,
    proj_id: str,
    region: str,
    project_instance: str,
    forwarder_id: str) -> Mapping[str, Any]:
  """Imports logs to Chronicle using the GCP CLOUDAUDIT log type.

  Args:
    http_session: Authorized session for HTTP requests.
    logs_file: File-like object containing the logs to import.
    proj_id: Google Cloud project ID.
    region: Chronicle region.
    project_instance: Chronicle instance.
    forwarder_id: UUID4 of the forwarder.

  Returns:
    dict: JSON response from the API.

  Raises:
    requests.HTTPError: If the request fails.
  """
  log_type = "GCP_CLOUDAUDIT"
  parent = (f"projects/{proj_id}/"
            f"locations/{region}/"
            f"instances/{project_instance}/"
            f"logTypes/{log_type}")
  url = (f"https://{region}-chronicle.googleapis.com/"
         f"v1alpha/{parent}/logs:import")
  logs = logs_file.read()
  # Reset file pointer to beginning in case it needs to be read again
  logs_file.seek(0)
  logs = base64.b64encode(logs.encode("utf-8")).decode("utf-8")
  now = datetime.datetime.now(datetime.timezone.utc).isoformat()
  body = {
      "inline_source": {
          "logs": [
              {
                  "data": logs,
                  "log_entry_time": now,
                  "collection_time": now,
              }
          ],
          "forwarder": (f"projects/{proj_id}/"
                        f"locations/{region}/"
                        f"instances/{project_instance}/"
                        f"forwarders/{forwarder_id}")
      }
  }
  response = http_session.request("POST", url, json=body)
  if response.status_code >= 400:
    logging.error("Error response: %s", response.text)
  response.raise_for_status()
  logging.info("Request successful with status code: %d", response.status_code)
  return response.json()


def main():
  """Main entry point for the logs import script."""
  # Configure logging
  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  )
  logger = logging.getLogger(__name__)

  parser = argparse.ArgumentParser(description="Import logs to Chronicle.")
  # common
  chronicle_auth.add_argument_credentials_file(parser)
  project_instance.add_argument_project_instance(parser)
  project_id.add_argument_project_id(parser)
  regions.add_argument_region(parser)
  # local
  parser.add_argument(
      "--forwarder_id",
      type=str,
      required=True,
      help="UUID4 of the forwarder")
  parser.add_argument(
      "--logs_file",
      type=argparse.FileType("r"),
      required=True,
      help="path to a log file (or \"-\" for STDIN)")
  args = parser.parse_args()
  auth_session = chronicle_auth.initialize_http_session(
      args.credentials_file,
      SCOPES,
  )
  try:
    result = logs_import(
        auth_session,
        args.logs_file,
        args.project_id,
        args.region,
        args.project_instance,
        args.forwarder_id
    )
    logging.info("Import operation completed successfully")
    print(json.dumps(result, indent=2))
  except Exception as e:  # pylint: disable=broad-except
    logging.error("Import operation failed: %s", str(e))
    return 1
  return 0


if __name__ == "__main__":
    main()
