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
r"""Executable and reusable sample for updating an Alert.

Usage:
  python -m alerts.v1alpha.update_alert \
    --project_id=<PROJECT_ID>   \
    --project_instance=<PROJECT_INSTANCE> \
    --alert_id=<ALERT_ID> \
    --priority=<PRIORITY> \
    --reason=<REASON> \
    --reputaion=<REPUTATION> \
    --priority=<PRIORITY> \
    --status=<STATUS> \
    --verdict=<VERDICT>

API reference:
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.legacy/legacyUpdateAlert
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/Noun#Priority
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/Noun#Reason
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/Noun#Reputation
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/Noun#Priority
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/Noun#Status
  https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/Noun#Verdict
"""

import argparse
import json
from typing import Dict

from common import chronicle_auth
from common import project_id
from common import project_instance
from common import regions

from google.auth.transport import requests

CHRONICLE_API_BASE_URL = "https://chronicle.googleapis.com"
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
]

PRIORITY_ENUM = (
    "PRIORITY_UNSPECIFIED",
    "PRIORITY_INFO",
    "PRIORITY_LOW",
    "PRIORITY_MEDIUM",
    "PRIORITY_HIGH",
    "PRIORITY_CRITICAL",
)
REASON_ENUM = (
    "REASON_UNSPECIFIED",
    "REASON_NOT_MALICIOUS",
    "REASON_MALICIOUS",
    "REASON_MAINTENANCE",
)
REPUTATION_ENUM = (
    "REPUTATION_UNSPECIFIED",
    "USEFUL",
    "NOT_USEFUL",
)
STATUS_ENUM = (
    "STATUS_UNSPECIFIED",
    "NEW",
    "REVIEWED",
    "CLOSED",
    "OPEN",
)
VERDICT_ENUM = (
    "VERDICT_UNSPECIFIED",
    "TRUE_POSITIVE",
    "FALSE_POSITIVE",
)


def update_alert(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    alert_id: str,
    confidence: int,
    reason: str,
    reputation: str,
    priority: str,
    status: str,
    verdict: str,
    ) -> Dict[str, any]:
  """Gets an Alert.

  Args:
    http_session: Authorized session for HTTP requests.
    proj_id: GCP project id or number to which the target instance belongs.
    proj_instance: Customer ID (uuid with dashes) for the Chronicle instance.
    proj_region: region in which the target project is located.
    alert_id: identifier for the alert
    confidence: confidence score (0-100) of the finding
    reason: reason for closing an Alert
    reputaion: A categorization of the finding as useful or not useful
    priority: alert priority.
    status: status of the alert
    verdict: verdict of the alert

  Returns:
    Dictionary representation of the Alert

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
  url = f"{base_url_with_region}/v1alpha/{parent}/legacy:legacyUpdateAlert/"

  feedback = { }
        # "idp_user_id": "admin@dandye.altostrat.com",  # readonly
        # "create_time": string,  # readonly

        #"confidence_score": confidence,
        #"reason": reason,
        #"reputation": reputation,
        #"priority": priority,
        #"status": status,
        #"verdict": verdict,

        #"risk_score": integer,
        #"disregarded": boolean,
        #"severity": integer,
        #"comment": string,
        #"root_cause": string,
        #"reason": enum (Reason),
        #"severity_display": string

  if confidence:
    feedback["confidence_score"] = confidence
  if reason:
    feedback["reason"] = reason
  if reputation:
    feedback["reputation"] = reputation
  if priority:
    feedback["priority"] = priority
  if status:
    feedback["status"] = status
  if verdict:
    feedback["verdict"] = verdict

  payload = {
    "alert_id": alert_id,
    "feedback": feedback,
  }

  response = http_session.request("POST", url, json=payload)

  # Expected server response is described in:
  # https://cloud.google.com/chronicle/docs/reference/rest/v1alpha/projects.locations.instances.legacy/legacyUpdateAlert
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
      "--alert_id", type=str, required=True,
      help="identifier for the alert"
  )
  parser.add_argument(
      "-d", "--include-detections", type=bool, default=False,required=False,
      help="flag to include detections"
  )
  parser.add_argument(
      "--confidence_score",
      type=int,
      required=False,
      help="confidence score (0-100) of the finding",
  )
  parser.add_argument(
      "--priority",
      choices=PRIORITY_ENUM,
      required=False,
      help="alert priority.",
  )
  parser.add_argument(
      "--reason",
      choices=REASON_ENUM,
      required=False,
      help="reason for closing an Alert",
  )
  parser.add_argument(
      "--reputation",
      choices=REPUTATION_ENUM,
      required=False,
      help="A categorization of the finding as useful or not useful",
  )
  parser.add_argument(
      "--status",
      choices=STATUS_ENUM,
      required=False,
      help="alert status",
  )
  parser.add_argument(
      "--verdict",
      choices=VERDICT_ENUM,
      required=False,
      help="a verdict on whether the finding reflects a security incident",
  )
  args = parser.parse_args()

  # Check if at least one of the specific arguments is provided
  if not any([args.priority, args.reason, args.reputation, args.status, args.verdict]):
    parser.error("At least one of the arguments --priority, --reason, --reputation, --status, or --verdict is required.")

  auth_session = chronicle_auth.initialize_http_session(
      args.credentials_file,
      SCOPES,
  )
  a_list = update_alert(
      auth_session,
      args.project_id,
      args.project_instance,
      args.region,
      args.alert_id,
      args.confidence_score,
      args.reason,
      args.reputation,
      args.priority,
      args.status,
      args.verdict,
  )
  print(json.dumps(a_list, indent=2))
