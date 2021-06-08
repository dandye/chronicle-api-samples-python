#!/usr/bin/env python3

# Copyright 2021 Google LLC
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
"""Executable and reusable sample for archiving a detection rule."""

import argparse

from google.auth.transport import requests

from common import chronicle_auth

CHRONICLE_API_BASE_URL = "https://backstory.googleapis.com"


def archive_rule(http_session: requests.AuthorizedSession, version_id: str):
  """Archives a detection rule.

  Archiving a rule will fail if:
  - The provided version is not the latest rule version
  - The rule is enabled as live
  - The rule has retrohunts in progress

  If alerting is enabled for a rule, archiving the rule will automatically
  disable alerting for the rule.

  Args:
    http_session: Authorized session for HTTP requests.
    version_id: Unique ID of the detection rule to archive ("ru_<UUID>" or
      "ru_<UUID>@v_<seconds>_<nanoseconds>"). If a version suffix isn't
      specified we use the rule's latest version.

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).
  """
  url = f"{CHRONICLE_API_BASE_URL}/v2/detect/rules/{version_id}:archive"

  response = http_session.request("POST", url)
  # Expected server response:
  # {}

  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  chronicle_auth.add_argument_credentials_file(parser)
  parser.add_argument(
      "-vi",
      "--version_id",
      type=str,
      required=True,
      help="version ID ('ru_<UUID>[@v_<seconds>_<nanoseconds>]')")

  args = parser.parse_args()
  session = chronicle_auth.initialize_http_session(args.credentials_file)
  archive_rule(session, args.version_id)
