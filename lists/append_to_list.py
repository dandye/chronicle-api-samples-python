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
"""Executable and reusable sample for appending to a list."""

import argparse
from typing import Sequence

from common import chronicle_auth
from common import regions

from google.auth.transport import requests

from . import get_list

BACKSTORY_API_BASE_URL = "https://backstory.googleapis.com"


# pylint: disable=bad-continuation
def append_to_list(http_session: requests.AuthorizedSession,
                   list_api_url: str,
                   list_id: str,
                   content_lines: Sequence[str]) -> str:
  """Append items to an existing reference list.

  Args:
    http_session: Authorized session for HTTP requests.
    list_api_url: Regionalizied API endpoint.
    list_id: ID of existing list.
    content_lines: Iterable containing items to append to the existing list.

  Returns:
    List update timestamp.

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).
  """
  current_list = get_list.get_list(http_session, list_id)
  seen = set(current_list)
  deduplicated_list = [x for x in content_lines
                       if not (x in seen or seen.add(x))]
  content_lines = current_list + deduplicated_list

  body = {
      "name": list_id,
      "lines": content_lines,
  }
  update_fields = ["list.lines"]
  params = {"update_mask": ",".join(update_fields)}

  response = http_session.request("PATCH",
                                  list_api_url,
                                  params=params,
                                  json=body)
  # Expected server response:
  # {
  #   "name": "<list name>",
  #   "description": "<list description>",
  #   "createTime": "yyyy-mm-ddThh:mm:ss.ssssssZ",
  #   "lines": [
  #     "<line 1>",
  #     "<line 2>",
  #     ...
  #   ],
  #   "contentType": "<content type. omitted if type is STRING list.>"
  # }

  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()
  return response.json()["createTime"]


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  chronicle_auth.add_argument_credentials_file(parser)
  regions.add_argument_region(parser)
  parser.add_argument(
      "-n", "--name", type=str, required=True, help="unique name for the list")
  parser.add_argument(
      "-f",
      "--list_file",
      type=argparse.FileType("r"),
      required=True,
      # File example:
      #   python3 -m lists.append_to_list <other args> -f <path>
      # STDIN example:
      #   cat <path> | python3 -m lists.append_to_list <other args> -f -
      help="path to file containing the list content to append, or - for STDIN")
  args = parser.parse_args()

  session = chronicle_auth.initialize_http_session(args.credentials_file)
  api_url = f"{regions.url(BACKSTORY_API_BASE_URL, args.region)}/v2/lists"
  new_list_create_time = append_to_list(
      session,
      api_url,
      args.name,
      args.list_file.read().splitlines()
  )
  print(f"List successfully appended at {new_list_create_time}")
