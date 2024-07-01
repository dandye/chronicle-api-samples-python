#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import json
import time
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


def legacy_get_alert(
    http_session: requests.AuthorizedSession,
    proj_id: str,
    proj_instance: str,
    proj_region: str,
    alert_id: str,
) -> Dict[str, any]:
  """Get Alert details (legacy).

  Args:
    http_session: Authorized session for HTTP requests.
    proj_id: GCP project id or number to which the target instance belongs.
    proj_instance: Customer ID (uuid with dashes) for the Chronicle instance.
    proj_region: region in which the target project is located.
    alert_id: identifier for the alert to get.
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
  url = f"{base_url_with_region}/v1alpha/{parent}/legacy:legacyGetAlert"

  params = {
    "alertId": alert_id,
  }

  response = http_session.request("GET", url, params=params)

  if response.status_code >= 400:
    print(response.text)
  response.raise_for_status()
  return response.json()


if __name__ == "__main__":

  now = datetime.now()
  fifteen_days_ago = now - timedelta(days=15)

  parser = argparse.ArgumentParser()
  chronicle_auth.add_argument_credentials_file(parser)
  project_instance.add_argument_project_instance(parser)
  project_id.add_argument_project_id(parser)
  regions.add_argument_region(parser)
  parser.add_argument(
      "--alert_id", type=str, required=True,
      help="Id for the alert"
  )
  args = parser.parse_args()

  auth_session = chronicle_auth.initialize_http_session(
      args.credentials_file,
      SCOPES,
  )
  alerts = legacy_get_alert(
      auth_session,
      args.project_id,
      args.project_instance,
      args.region,
      args.alert_id,
  )
  print(json.dumps(alerts, indent=2))
