# Chronicle API Samples in Python

Python samples and guidelines for using Chronicle APIs.

## Setup

Follow these instructions: https://cloud.google.com/python/setup

You may skip installing the Cloud Client Libraries and the Cloud SDK, they are
unnecessary for interacting with Chronicle.

After creating and activating a virtual environment, install Python
library dependencies by running this command:

```shell
pip install -r requirements.txt
```

It is assumed that you're using Python 3.7 or above. If you're using an older
Python 3 version, you need to install this backported library as well:

```shell
pip install dataclasses
```

## Credentials

Running the samples requires a JSON credentials file. By default, all the
samples try to use the file `.chronicle_credentials.json` in the user's home
directory. If this file is not found, you need to specify it explicitly by
adding the following argument to the sample's command-line:

```shell
-c <file_path>
```

or

```shell
--credentials_file <file_path>
```

## Usage

You can run samples on the command-line, assuming the current working directory
is the root directory of this repository (i.e. the directory which contains
this `README.md` file):

### Detect API

```shell
python3 -m detect.v2.<sample_name> -h
```

### Lists API

```shell
python3 -m lists.<sample_name> -h
```

### Lists API v1alpha

```shell
python -m lists.v1alpha.create_list -h
python -m lists.v1alpha.get_list -h
python -m lists.v1alpha.patch_list -h
```

## SDK CLI Wrapper

In addition to running individual sample scripts, you can use the unified CLI wrapper that provides access to all Chronicle APIs through a single command-line interface.

### Installation

Install the SDK in development mode:

```shell
pip install -e .
```

This will install the `chronicle` command-line tool.

### Usage

The CLI follows this general pattern:
```shell
chronicle [common options] COMMAND_GROUP COMMAND [command options]
```

Common options (required for all commands):
- `--credentials-file`: Path to service account credentials file
- `--project-id`: GCP project id or number
- `--project-instance`: Customer ID for the Chronicle instance
- `--region`: Region of the target project

Available command groups:

1. Detection API (`detect`):
```shell
# Get an alert
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  detect get-alert --alert-id <id>

# Get a detection
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  detect get-detection --detection-id <id>
```

2. Ingestion API (`ingestion`):
```shell
# Import events
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  ingestion import-events --json-events '<events_json>'

# Get an event
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  ingestion get-event --event-id <id>

# Batch get events
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  ingestion batch-get-events --event-ids '[<id1>,<id2>]'
```

3. Search API (`search`):
```shell
# Find asset events
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  search find-asset-events --asset-indicator <indicator> --start-time <time> --end-time <time>

# Find raw logs
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  search find-raw-logs --query <query>

# Find UDM events
chronicle --credentials-file creds.json --project-id proj --project-instance inst --region reg \
  search find-udm-events --tokens <token1> --tokens <token2>
```

For detailed help on any command:
```shell
chronicle --help                    # General help
chronicle COMMAND_GROUP --help      # Help for a command group
chronicle COMMAND_GROUP CMD --help  # Help for a specific command
