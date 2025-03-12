# Lists Examples

## Lists Help
```
❯ chronicle lists --help
Usage: chronicle lists [OPTIONS] COMMAND [ARGS]...

  Lists API commands.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new list.
  get     Get a list by ID.
  patch   Update an existing list.

```

## Create a List

### Help for `chronicle lists create`
```
❯ chronicle lists create --help
Usage: chronicle lists create [OPTIONS]

  Create a new list.

Options:
  --region TEXT            Region in which the target project is located. Can
                           also be set via CHRONICLE_REGION env var.
  --project-instance TEXT  Customer ID (uuid with dashes) for the Chronicle
                           instance. Can also be set via CHRONICLE_INSTANCE
                           env var.
  --project-id TEXT        GCP project id or number. Can also be set via
                           CHRONICLE_PROJECT_ID env var.
  --credentials-file TEXT  Path to service account credentials file. Can also
                           be set via CHRONICLE_CREDENTIALS_FILE env var.
  --env-file TEXT          Path to .env file containing configuration
                           variables.
  --name TEXT              Name of the list to create.  [required]
  --description TEXT       Description of the list.
  --lines TEXT             JSON array of strings to add to the list.
                           [required]
  --help                   Show this message and exit.
```

### Example Usage for `chronicle lists create`
```
❯ chronicle lists create \
  --name "Blocked IPs" \
  --description "List of blocked IP addresses" \
  --lines '["192.168.1.1", "10.0.0.1", "172.16.0.1"]'
{
  "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/lists/Blocked IPs",
  "createTime": "2025-03-12T14:00:00Z",
  "description": "List of blocked IP addresses",
  "lines": [
    "192.168.1.1",
    "10.0.0.1",
    "172.16.0.1"
  ]
}
```

## Get a List

### Help for `chronicle lists get`
```
❯ chronicle lists get --help
Usage: chronicle lists get [OPTIONS]

  Get a list by ID.

Options:
  --region TEXT            Region in which the target project is located. Can
                           also be set via CHRONICLE_REGION env var.
  --project-instance TEXT  Customer ID (uuid with dashes) for the Chronicle
                           instance. Can also be set via CHRONICLE_INSTANCE
                           env var.
  --project-id TEXT        GCP project id or number. Can also be set via
                           CHRONICLE_PROJECT_ID env var.
  --credentials-file TEXT  Path to service account credentials file. Can also
                           be set via CHRONICLE_CREDENTIALS_FILE env var.
  --env-file TEXT          Path to .env file containing configuration
                           variables.
  --list-id TEXT           ID of the list to retrieve.  [required]
  --help                   Show this message and exit.
```

### Example Usage for `chronicle lists get`
```
❯ chronicle lists get \
  --list-id "Blocked IPs"
{
  "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/lists/Blocked IPs",
  "createTime": "2025-03-12T14:00:00Z",
  "description": "List of blocked IP addresses",
  "lines": [
    "192.168.1.1",
    "10.0.0.1",
    "172.16.0.1"
  ]
}
```

## Update a List

### Help for `chronicle lists patch`
```
❯ chronicle lists patch --help
Usage: chronicle lists patch [OPTIONS]

  Update an existing list.

Options:
  --region TEXT            Region in which the target project is located. Can
                           also be set via CHRONICLE_REGION env var.
  --project-instance TEXT  Customer ID (uuid with dashes) for the Chronicle
                           instance. Can also be set via CHRONICLE_INSTANCE
                           env var.
  --project-id TEXT        GCP project id or number. Can also be set via
                           CHRONICLE_PROJECT_ID env var.
  --credentials-file TEXT  Path to service account credentials file. Can also
                           be set via CHRONICLE_CREDENTIALS_FILE env var.
  --env-file TEXT          Path to .env file containing configuration
                           variables.
  --list-id TEXT           ID of the list to update.  [required]
  --description TEXT       New description for the list.
  --lines-to-add TEXT      JSON array of strings to add to the list.
  --lines-to-remove TEXT   JSON array of strings to remove from the list.
  --help                   Show this message and exit.
```

### Example Usage for `chronicle lists patch`
```
❯ chronicle lists patch \
  --list-id "Blocked IPs" \
  --description "Updated list of blocked IP addresses" \
  --lines-to-add '["8.8.8.8"]' \
  --lines-to-remove '["172.16.0.1"]'
{
  "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/lists/Blocked IPs",
  "createTime": "2025-03-12T14:00:00Z",
  "updateTime": "2025-03-12T15:30:00Z",
  "description": "Updated list of blocked IP addresses",
  "lines": [
    "192.168.1.1",
    "10.0.0.1",
    "8.8.8.8"
  ]
}
```

### Example Usage for `-m lists.v1alpha.patch_list`
```
❯ python3 -m lists.v1alpha.patch_list --help
usage: patch_list.py [-h] [-c CREDENTIALS_FILE] -i PROJECT_INSTANCE -p PROJECT_ID
                     [-r {asia-northeast1,asia-south1,asia-southeast1,australia-southeast1,eu,europe,europe-west12,europe-west2,europe-west3,europe-west6,europe-west9,me-central1,me-central2,me-west1,northamerica-northeast2,southamerica-east1,us}]
                     --list_id LIST_ID [--description DESCRIPTION] [--lines_to_add LINES_TO_ADD]
                     [--lines_to_remove LINES_TO_REMOVE]

options:
  -h, --help            show this help message and exit
  -c CREDENTIALS_FILE, --credentials_file CREDENTIALS_FILE
                        credentials file path (default: '/Users/dandye/.chronicle_credentials.json')
  -i PROJECT_INSTANCE, --project_instance PROJECT_INSTANCE
                        Customer ID for Chronicle instance
  -p PROJECT_ID, --project_id PROJECT_ID
                        Your BYOP, project id
  -r {asia-northeast1,asia-south1,asia-southeast1,australia-southeast1,eu,europe,europe-west12,europe-west2,europe-west3,europe-west6,europe-west9,me-central1,me-central2,me-west1,northamerica-northeast2,southamerica-east1,us}, --region {asia-northeast1,asia-south1,asia-southeast1,australia-southeast1,eu,europe,europe-west12,europe-west2,europe-west3,europe-west6,europe-west9,me-central1,me-central2,me-west1,northamerica-northeast2,southamerica-east1,us}
                        the region where the customer is located (default: us)
  --list_id LIST_ID     ID of the list to update
  --description DESCRIPTION
                        New description for the list
  --lines_to_add LINES_TO_ADD
                        JSON array of strings to add to the list
  --lines_to_remove LINES_TO_REMOVE
                        JSON array of strings to remove from the list
```

```
❯ PROJECT_INSTANCE=3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d
PROJECT_ID=my-project
python3 -m lists.v1alpha.patch_list \
 --project_instance=$PROJECT_INSTANCE  \
 --project_id=$PROJECT_ID \
 --list_id "Blocked IPs" \
 --description "Updated list of blocked IP addresses" \
 --lines_to_add '["8.8.8.8"]' \
 --lines_to_remove '["172.16.0.1"]'
{
  "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/lists/Blocked IPs",
  "createTime": "2025-03-12T14:00:00Z",
  "updateTime": "2025-03-12T15:30:00Z",
  "description": "Updated list of blocked IP addresses",
  "lines": [
    "192.168.1.1",
    "10.0.0.1",
    "8.8.8.8"
  ]
}
```