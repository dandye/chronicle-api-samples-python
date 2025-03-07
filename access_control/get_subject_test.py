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
"""Unit tests for the "get_subject" module."""

import unittest
import argparse

from unittest import mock

from google.auth.transport import requests

from . import get_subject


class GetSubjectTest(unittest.TestCase):

  def test_initialize_command_line_args(self):
    actual = get_subject.initialize_command_line_args([
        "--name=test@test.com",
    ])
    self.assertEqual(
        actual,
        argparse.Namespace(
            credentials_file=None, name="test@test.com", region="us"))

  @mock.patch.object(requests, "AuthorizedSession", autospec=True)
  @mock.patch.object(requests.requests, "Response", autospec=True)
  def test_get_subject_error(self, mock_response, mock_session):
    mock_session.request.return_value = mock_response
    type(mock_response).status_code = mock.PropertyMock(return_value=400)
    mock_response.raise_for_status.side_effect = (
        requests.requests.exceptions.HTTPError())

    with self.assertRaises(requests.requests.exceptions.HTTPError):
      get_subject.get_subject(mock_session, "")

  @mock.patch.object(requests, "AuthorizedSession", autospec=True)
  @mock.patch.object(requests.requests, "Response", autospec=True)
  def test_get_subject(self, mock_response, mock_session):
    mock_session.request.return_value = mock_response
    type(mock_response).status_code = mock.PropertyMock(return_value=200)
    subject_id = "test@test.com"
    expected = {
        "subject": {
            "name":
                subject_id,
            "type":
                "SUBJECT_TYPE_ANALYST",
            "roles": [{
                "name":
                    "Test",
                "title":
                    "Test role",
                "description":
                    "The Test role",
                "createTime":
                    "2020-11-05T00:00:00Z",
                "isDefault":
                    False,
                "permissions": [{
                    "name": "Test",
                    "title": "Test permission",
                    "description": "The Test permission",
                    "createTime": "2020-11-05T00:00:00Z",
                },]
            },]
        },
    }
    mock_response.json.return_value = expected
    actual = get_subject.get_subject(mock_session, subject_id)
    self.assertEqual(actual, expected)


if __name__ == "__main__":
  unittest.main()
