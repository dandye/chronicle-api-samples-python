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


def legacy_update_alert(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    alert_id: str,
) -> str:
  """Legacy Update an Alert.

  Args:
    http_session: Authorized session for HTTP requests.
    proj_id: GCP project id or number to which the target instance belongs.
    proj_instance: Customer ID (uuid with dashes) for the Chronicle instance.
    proj_region: region in which the target project is located.
    alert_id: identifier for the alert to be closed.

  Returns:
    ...

  Raises:
    requests.exceptions.HTTPError: HTTP request resulted in an error
      (response.status_code >= 400).
  """

  # pylint: disable=line-too-long
  parent = f"projects/{proj_id}/locations/{proj_region}/instances/{proj_instance}"
  url = f"https://{proj_region}-chronicle.googleapis.com/v1alpha/{parent}/legacy:legacyUpdateAlert"
  # pylint: enable=line-too-long

  body = {
      "alertId": alert_id,
      "feedback":{
        "verdict": "VERDICT_UNSPECIFIED",
        "reputation": "REPUTATION_UNSPECIFIED",
        "comment": "automated cleanup",
        "status": "CLOSED",
        "rootCause": "Other",
        "reason": "REASON_MAINTENANCE"
      },
  }
  url_w_query_string = f"{url}"
  response = http_session.request("POST", url_w_query_string, json=body)

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
  parser.add_argument("--alert_id",
                      type=str,
                      default=None,
                      required=False,
                      help="ID of the Alert.")
  parser.add_argument("--alert_ids_file",
                      type=str,
                      default=None,
                      required=False,
                      help="File with one Alert ID per line.")

  args = parser.parse_args()

  # pylint: disable-next=line-too-long
  auth_session = chronicle_auth.initialize_http_session(args.credentials_file, SCOPES)
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

