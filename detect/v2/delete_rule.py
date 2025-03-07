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
"""Executable and reusable sample for deleting a detection rule.

API reference:
https://cloud.google.com/chronicle/docs/reference/detection-engine-api#deleterule
"""

import argparse

from google.auth.transport import requests

from common import chronicle_auth
from common import regions

CHRONICLE_API_BASE_URL = "https://backstory.googleapis.com"


def delete_rule(http_session: requests.AuthorizedSession, rule_id: str):
  """Delete a specific detection rule.

  Args:
    http_session: Authorized session for HTTP requests.
    rule_id: Unique ID of the detection rule to delete ("ru_<UUID>"). It does
      not accept version id format ("ru_<UUID>@v_<seconds>_<nanoseconds>").

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).
  """
  url = f"{CHRONICLE_API_BASE_URL}/v2/detect/rules/{rule_id}"

  response = http_session.request("DELETE", url)
  # Expected server response:
  # {}

  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  chronicle_auth.add_argument_credentials_file(parser)
  regions.add_argument_region(parser)
  parser.add_argument(
      "-ri", "--rule_id", type=str, required=True, help="rule ID ('ru_<UUID>')")

  args = parser.parse_args()
  CHRONICLE_API_BASE_URL = regions.url(CHRONICLE_API_BASE_URL, args.region)
  session = chronicle_auth.initialize_http_session(args.credentials_file)
  delete_rule(session, args.rule_id)
