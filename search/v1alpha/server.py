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
"""Model Context Protocol Server for Search API."""

import json
from typing import Dict, List, Optional
from concurrent import futures
from datetime import datetime

import grpc
from google.protobuf import empty_pb2
from google.auth.transport import requests

from . import asset_events_find
from . import raw_logs_find
from . import udm_events_find


class SearchServicer:
  """Implements the Search API server."""

  def __init__(self, http_session: requests.AuthorizedSession, proj_id: str,
               proj_instance: str, proj_region: str):
    """Initialize the servicer with authentication and project details.

        Args:
            http_session: Authorized session for HTTP requests
            proj_id: GCP project ID
            proj_instance: Chronicle instance ID
            proj_region: GCP region
        """
    self.http_session = http_session
    self.proj_id = proj_id
    self.proj_instance = proj_instance
    self.proj_region = proj_region

  def FindAssetEvents(self, request, context):
    """Find asset events in Chronicle."""
    try:
      result = asset_events_find.find_asset_events(
          http_session=self.http_session,
          proj_id=self.proj_id,
          proj_instance=self.proj_instance,
          proj_region=self.proj_region,
          asset_indicator=request.asset_indicator,
          start_time=request.start_time,
          end_time=request.end_time,
          reference_time=request.reference_time
          if request.HasField('reference_time') else None,
          max_results=request.max_results
          if request.HasField('max_results') else None)
      return result
    except Exception as e:
      context.set_code(grpc.StatusCode.INTERNAL)
      context.set_details(str(e))
      return empty_pb2.Empty()

  def FindRawLogs(self, request, context):
    """Find raw logs in Chronicle."""
    try:
      result = raw_logs_find.find_raw_logs(
          http_session=self.http_session,
          proj_id=self.proj_id,
          proj_instance=self.proj_instance,
          proj_region=self.proj_region,
          query=request.query,
          batch_tokens=request.batch_tokens if request.batch_tokens else None,
          log_ids=request.log_ids if request.log_ids else None,
          regex_search=request.regex_search,
          case_sensitive=request.case_sensitive,
          max_response_size=request.max_response_size
          if request.HasField('max_response_size') else None)
      return result
    except Exception as e:
      context.set_code(grpc.StatusCode.INTERNAL)
      context.set_details(str(e))
      return empty_pb2.Empty()


def serve(http_session: requests.AuthorizedSession,
          proj_id: str,
          proj_instance: str,
          proj_region: str,
          port: int = 50051):
  """Start the gRPC server.

    Args:
        http_session: Authorized session for HTTP requests
        proj_id: GCP project ID
        proj_instance: Chronicle instance ID
        proj_region: GCP region
        port: Port number to listen on
    """
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  servicer = SearchServicer(http_session, proj_id, proj_instance, proj_region)
  # Register the servicer
  # Note: The actual registration would depend on the generated proto service
  # server.add_Search_servicer_to_server(servicer, server)

  server.add_insecure_port(f'[::]:{port}')
  server.start()
  server.wait_for_termination()
