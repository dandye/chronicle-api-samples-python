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
"""Setup configuration for Chronicle API SDK."""

from setuptools import find_packages
from setuptools import setup

setup(
    name="chronicle-api",
    version="0.1.3",
    description="Chronicle API SDK and CLI",
    author="Google LLC",
    author_email="chronicle-support@google.com",
    packages=find_packages(include=[
        'common',
        'sdk', 'sdk.*',
        'detect.v1alpha', 'detect.v1alpha.*',
        'ingestion.v1alpha', 'ingestion.v1alpha.*',
        'iocs.v1alpha', 'iocs.v1alpha.*',
        'lists.v1alpha', 'lists.v1alpha.*',
        'search.v1alpha', 'search.v1alpha.*',
    ]),
    install_requires=[
        "click>=8.0.0",
        "google-auth>=2.0.0",
        "requests>=2.25.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": ["chronicle=sdk.cli:cli",],
    },
    exclude_package_data={"": [".gitignore"]},
    python_requires=">=3.10",
    license="Apache 2.0",
)
