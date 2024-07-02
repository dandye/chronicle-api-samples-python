#!/usr/bin/env python3

import argparse
import json

from google.auth.transport import requests

from common import chronicle_auth
from common import project_id
from common import project_instance
from common import regions

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
DEFAULT_FEEDBACK = {
    # These use a controlled vocab. See enums above.
    "reason": "REASON_MAINTENANCE",
    "reputation": "REPUTATION_UNSPECIFIED",
    "status": "CLOSED",
    "verdict": "VERDICT_UNSPECIFIED",
    # free text (not controlled vocab)
    "comment": "automated cleanup",
    "rootCause": "Other",
}


def legacy_update_alert(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    alert_id: str,
    feedback: dict=None,
) -> str:
  """Legacy Update an Alert.

  Args:
    http_session: Authorized session for HTTP requests.
    proj_id: GCP project id or number to which the target instance belongs.
    proj_instance: Customer ID (uuid with dashes) for the Chronicle instance.
    proj_region: region in which the target project is located.
    alert_id: identifier for the alert to be closed.
    feedback: dictionary containing the feedback key/values.

  Returns:
    response.json

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).
  """
  # pylint: disable=line-too-long
  parent = f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}"
  url = f"https://{proj_region}-chronicle.googleapis.com/v1alpha/{parent}/legacy:legacyUpdateAlert"
  # pylint: enable=line-too-long

  if not feedback:
    feedback = {}
  reason = feedback.get("reason") or DEFAULT_FEEDBACK["reason"]
  reputation = feedback.get("reputation") or DEFAULT_FEEDBACK["reputation"]
  status = feedback.get("status") or DEFAULT_FEEDBACK["status"]
  verdict = feedback.get("verdict") or DEFAULT_FEEDBACK["verdict"]

  # enum validation
  if reason not in REASON_ENUM:
    raise ValueError(f"Reason {reason} not in {REASON_ENUM}")
  if reputation not in REPUTATION_ENUM:
    raise ValueError(f"Reputation {reputation} not in {REPUTATION_ENUM}")
  if status not in STATUS_ENUM:
    raise ValueError(f"Status {status} not in {STATUS_ENUM}")
  if verdict not in VERDICT_ENUM:
    raise ValueError(f"Verdict {verdict} not in {VERDICT_ENUM}")

  comment = feedback.get("comment") or DEFAULT_FEEDBACK["comment"]
  root_cause = feedback.get("rootCause") or DEFAULT_FEEDBACK["rootCause"]

  body = {
      "alertId": alert_id,
      "feedback": {
          "comment": comment,
          "reason": reason,
          "reputation": reputation,
          "rootCause": root_cause,
          "status": status,
          "verdict": verdict,
      },
  }
  response = http_session.request("POST", url, json=body)
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
  # local
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("--alert_id",
                      type=str,
                      help="ID of the Alert.")
  group.add_argument("--alert_ids_file",
                      type=str,
                      help="File with one Alert ID per line.")
  args = parser.parse_args()

  # pylint: disable-next=line-too-long
  auth_session = chronicle_auth.initialize_http_session(
      args.credentials_file,
      SCOPES
  )
  if args.alert_id:
    response = legacy_update_alert(
        auth_session,
        args.project_id,
        args.project_instance,
        args.region,
        args.alert_id,
    )
    print(json.dumps(response, indent=2))
  elif args.alert_ids_file:
    with open(args.alert_ids_file) as fh:
      for an_id in fh.readlines():
        print(f"working on alert id: {an_id}")
        response = legacy_update_alert(
            auth_session,
            args.project_id,
            args.project_instance,
            args.region,
            an_id.strip(),
        )
        print(json.dumps(response, indent=2))
