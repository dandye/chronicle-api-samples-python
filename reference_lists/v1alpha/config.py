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
"""Configuration for Reference Lists MCP client."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MCPConfig:
  """Configuration for MCP client.
    
    Attributes:
        host: Server hostname
        port: Server port number
        use_tls: Whether to use TLS for connection
        ca_cert: Path to CA certificate file for TLS
        client_cert: Path to client certificate file for TLS
        client_key: Path to client private key file for TLS
    """
  host: str = 'localhost'
  port: int = 50051
  use_tls: bool = False
  ca_cert: Optional[str] = None
  client_cert: Optional[str] = None
  client_key: Optional[str] = None

  @property
  def target(self) -> str:
    """Get the target address for gRPC connection.
        
        Returns:
            String in format "host:port"
        """
    return f"{self.host}:{self.port}"

  def get_channel_credentials(self) -> Optional[tuple]:
    """Get channel credentials for TLS connection.
        
        Returns:
            Tuple of (ca_cert, client_cert, client_key) if TLS is enabled,
            None otherwise.
        """
    if not self.use_tls:
      return None

    if not all([self.ca_cert, self.client_cert, self.client_key]):
      raise ValueError("TLS enabled but certificates not properly configured")

    return (self.ca_cert, self.client_cert, self.client_key)
