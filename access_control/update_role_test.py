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
"""Unit tests for the "update_role" module."""

import unittest
import argparse

from unittest import mock

from google.auth.transport import requests

from . import update_role


class UpdateRoleTest(unittest.TestCase):

  def test_initialize_command_line_args(self):
    actual = update_role.initialize_command_line_args(
        ["--name=Test", "--is-default=true"])
    self.assertEqual(
        actual,
        argparse.Namespace(
            credentials_file=None, name="Test", is_default=True, region="us"))

  @mock.patch.object(requests, "AuthorizedSession", autospec=True)
  @mock.patch.object(requests.requests, "Response", autospec=True)
  def test_update_role_error(self, mock_response, mock_session):
    mock_session.request.return_value = mock_response
    type(mock_response).status_code = mock.PropertyMock(return_value=400)
    mock_response.raise_for_status.side_effect = (
        requests.requests.exceptions.HTTPError())

    with self.assertRaises(requests.requests.exceptions.HTTPError):
      update_role.update_role(mock_session, "", False)

  @mock.patch.object(requests, "AuthorizedSession", autospec=True)
  @mock.patch.object(requests.requests, "Response", autospec=True)
  def test_update_role(self, mock_response, mock_session):
    mock_session.request.return_value = mock_response
    type(mock_response).status_code = mock.PropertyMock(return_value=200)
    role_id = "Test"
    is_default = True
    expected = {
        "name":
            "Test",
        "title":
            "Test role",
        "description":
            "The Test role",
        "createTime":
            "2020-11-05T00:00:00Z",
        "isDefault":
            True,
        "permissions": [{
            "name": "Test",
            "title": "Test permission",
            "description": "The Test permission",
            "createTime": "2020-11-05T00:00:00Z",
        },]
    }
    mock_response.json.return_value = expected
    actual = update_role.update_role(mock_session, role_id, is_default)
    self.assertEqual(actual, expected)


if __name__ == "__main__":
  unittest.main()
