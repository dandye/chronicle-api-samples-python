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

"""Chronicle Detection API commands."""

import json

import click
from common import chronicle_auth

from detect.v1alpha import get_alert
from detect.v1alpha import get_detection
from sdk.cli import add_common_options

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
]


@click.group()
def detect():
    """Detection API commands."""
    pass


@detect.command("get-alert")
@add_common_options
@click.option(
    "--alert-id",
    required=True,
    help="Identifier for the alert.",
)
@click.option(
    "--include-detections",
    is_flag=True,
    help="Include non-alerting detections.",
)
def get_alert_cmd(credentials_file, project_id, project_instance, region, alert_id, include_detections):
    """Get an alert by ID."""
    auth_session = chronicle_auth.initialize_http_session(
        credentials_file,
        SCOPES,
    )
    alert = get_alert.get_alert(
        auth_session,
        project_id,
        project_instance,
        region,
        alert_id,
        include_detections,
    )
    print(json.dumps(alert, indent=2))


@detect.command("get-detection")
@add_common_options
@click.option(
    "--detection-id",
    required=True,
    help="Identifier for the detection.",
)
def get_detection_cmd(credentials_file, project_id, project_instance, region, detection_id):
    """Get a detection by ID."""
    auth_session = chronicle_auth.initialize_http_session(
        credentials_file,
        SCOPES,
    )
    detection = get_detection.get_detection(
        auth_session,
        project_id,
        project_instance,
        region,
        detection_id,
    )
    print(json.dumps(detection, indent=2))
