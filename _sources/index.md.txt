# Chronicle API Samples in Python

Welcome to the documentation for Chronicle API Samples in Python. This project provides Python samples and guidelines for using Chronicle APIs, along with a unified command-line interface (CLI) for interacting with the Chronicle platform.

## Project Overview

This repository contains sample code and a REST API SDK for interacting with Google Chronicle, a cloud-native security analytics platform. The samples demonstrate how to use Chronicle's APIs for:

- Detection and alerting
- IoC (Indicators of Compromise) management
- Lists management
- Ingestion of security telemetry
- Search functionality

## Installation

### Setup

1. Follow the instructions at [https://cloud.google.com/python/setup](https://cloud.google.com/python/setup)
   - You may skip installing the Cloud Client Libraries and the Cloud SDK, as they're unnecessary for interacting with Chronicle.

2. After creating and activating a virtual environment, install Python library dependencies:
   ```shell
   pip install -r requirements.txt
   ```

3. Python 3.7 or above is recommended. For older Python 3 versions, install this backported library:
   ```shell
   pip install dataclasses
   ```

### Installing the Chronicle REST API SDK

Install the SDK from source:
```
python setup.py install
```

Alternatively, install the SDK from source using make:
```
make install
```

Build the wheel file:
```
make dist
```

## Credentials

Running the samples requires a JSON credentials file. By default, all samples try to use the file `.chronicle_credentials.json` in the user's home directory. If this file is not found, specify it explicitly:

```shell
-c <file_path>` or `--credentials_file <file_path>
```

## Usage

### Module Invocation

You can run samples directly as modules from the command line. For example:

```shell
# Detection API
python3 -m detect.v1alpha.get_detection -h

# Lists API
python3 -m lists.v1alpha.create_list -h
python3 -m lists.v1alpha.get_list -h
python3 -m lists.v1alpha.patch_list -h
```

### CLI Invocation

The SDK provides a unified command-line interface that follows this pattern:
```
chronicle [common options] COMMAND_GROUP COMMAND [command options]
```

#### Common Options

Common options can be provided either via command-line arguments or environment variables:

| CLI Option         | Environment Variable        | Description                   |
|--------------------|----------------------------|--------------------------------|
| --credentials-file | CHRONICLE_CREDENTIALS_FILE | Path to service account file   |
| --project-id       | CHRONICLE_PROJECT_ID       | GCP project id or number       |
| --project-instance | CHRONICLE_INSTANCE         | Chronicle instance ID (uuid)   |
| --region           | CHRONICLE_REGION           | Region where project is located|

### Using Environment Variables

You can set options in a `.env` file in your project root:

```bash
# .env file
CHRONICLE_CREDENTIALS_FILE=path/to/credentials.json
CHRONICLE_PROJECT_ID=your-project-id
CHRONICLE_INSTANCE=your-instance-id
CHRONICLE_REGION=your-region
```

The SDK will use values from the `.env` file or a file provided with the `--env-file` parameter. Command-line options take precedence over environment variables.

### Example Usage

```bash
# Get an alert (using environment variables)
chronicle detect alerts get --alert-id ABC123 --env-file=.env

# Create a list (specifying options directly)
chronicle lists create --name "blocklist" --description "Blocked IPs" \
 --lines '["1.1.1.1", "2.2.2.2"]' \
 --project-id your-project-id \
 --project-instance your-instance-id \
 --region us-central1
```

## API Documentation

Explore the detailed documentation for each API:

- [Detection API Examples](detect/detect_examples.md)
- [IoCs API Examples](iocs/iocs_examples.md)
- [Lists API Examples](lists/lists_examples.md)
- [Ingestion API Examples](ingestion/ingestion_examples.md)
- [Search API Examples](search/search_examples.md)

Each documentation page includes:
- Command help information
- Example command usage
- Sample responses
- Available options and parameters
