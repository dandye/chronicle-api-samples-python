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
"""Model Context Protocol Server for Reference Lists API."""

import json
from typing import Dict, List, Optional
from concurrent import futures

import grpc
from google.protobuf import empty_pb2
from google.auth.transport import requests

from . import create_reference_list
from . import get_reference_list
from . import list_reference_lists


class ReferenceListsServicer:
  """Implements the Reference Lists API server."""

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

  def CreateReferenceList(self, request, context):
    """Create a new reference list."""
    try:
      result = create_reference_list.create_reference_list(
          http_session=self.http_session,
          proj_id=self.proj_id,
          proj_instance=self.proj_instance,
          proj_region=self.proj_region,
          reference_list_id=request.reference_list_id,
          entries=request.entries,
          syntax_type=request.syntax_type,
          scope_names=request.scope_names
          if request.HasField('scope_names') else None,
          description=request.description
          if request.HasField('description') else None)
      return result
    except Exception as e:
      context.set_code(grpc.StatusCode.INTERNAL)
      context.set_details(str(e))
      return empty_pb2.Empty()

  def GetReferenceList(self, request, context):
    """Get a reference list by ID."""
    try:
      result = get_reference_list.get_reference_list(
          http_session=self.http_session,
          proj_id=self.proj_id,
          proj_instance=self.proj_instance,
          proj_region=self.proj_region,
          reference_list_id=request.reference_list_id)
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
  servicer = ReferenceListsServicer(http_session, proj_id, proj_instance,
                                    proj_region)
  # Register the servicer
  # Note: The actual registration would depend on the generated proto service
  # server.add_ReferenceLists_servicer_to_server(servicer, server)

  server.add_insecure_port(f'[::]:{port}')
  server.start()
  server.wait_for_termination()
