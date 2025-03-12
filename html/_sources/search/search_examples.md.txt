# Search Examples

## Search Help
```
❯ chronicle search --help
Usage: chronicle search [OPTIONS] COMMAND [ARGS]...

  Search API commands.

Options:
  --help  Show this message and exit.

Commands:
  find-asset-events    Find asset events within a time range.
  find-raw-logs        Find raw logs based on search criteria.
  find-udm-events      Find UDM events based on tokens or event IDs.
  get-search-query     Get a search query by ID.
  list-search-queries  List search queries for a specific user.

```

```
❯ chronicle search find-udm-events --help
Usage: chronicle search find-udm-events [OPTIONS]

  Find UDM events based on tokens or event IDs.

Options:
  --tokens TEXT                Optional list of tokens, with each token
                               referring to a group of UDM/Entity events.
  --event-ids TEXT             Optional list of UDM/Entity event ids that
                               should be returned.
  --return-unenriched-data     Return unenriched data.
  --return-all-events-for-log  Return all events generated from the ingested
                               log.
  --help                       Show this message and exit.
```


```
chronicle search find-udm-events \
  --tokens TEXT                Optional list of tokens, with each token
                               referring to a group of UDM/Entity events.
  --event-ids TEXT             Optional list of UDM/Entity event ids that
                               should be returned.
  --return-unenriched-data     Return unenriched data.
  --return-all-events-for-log  Return all events generated from the ingested
                               log.
```

```
❯ chronicle detect detections get --help
Usage: chronicle detect detections get [OPTIONS]

  Get a detection by ID.

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
  --detection-id TEXT      Identifier for the detection.  [required]
  --rule-id TEXT           Identifier for the rule that created the detection.
                           [required]
```

### Example Usage for `chronicle detect detections get`
```
❯ chronicle detect detections get \
  --detection-id "de_92092e71-3baa-0ebf-f230-4aacc5952c63" \
  --rule-id "ru_bf30236c-13af-4a85-a3af-5d58205e10f0"
{
  "type": "RULE_DETECTION",
  "detection": [
    {
      "ruleName": "ttp_powershell_decodebase64_ns139797",
      ...
```

### Example Usage for `-m detect.v1alpha.get_detection`
```
❯ python3 -m detect.v1alpha.get_detection --help
usage: get_detection.py [-h] [-c CREDENTIALS_FILE] -i PROJECT_INSTANCE -p PROJECT_ID
                        [-r {asia-northeast1,asia-south1,asia-southeast1,australia-southeast1,eu,europe,europe-west12,europe-west2,europe-west3,europe-west6,europe-west9,me-central1,me-central2,me-west1,northamerica-northeast2,southamerica-east1,us}]
                        --detection_id DETECTION_ID --rule_id RULE_ID

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
  --detection_id DETECTION_ID
                        Identifier for the detection
  --rule_id RULE_ID     Identifier for the rule that created the detection
```

```
❯ PROJECT_INSTANCE=7e977ce4-f45d-43b2-aea0-52f8b66acd80
PROJECT_ID=dandye-0324-chronicle
python3 -m detect.v1alpha.get_detection \
 --project_instance=$PROJECT_INSTANCE  \
 --project_id=$PROJECT_ID \
 --detection_id "de_92092e71-3baa-0ebf-f230-4aacc5952c63" \
 --rule_id "ru_bf30236c-13af-4a85-a3af-5d58205e10f0"
{
  "type": "RULE_DETECTION",
  "detection": [
    {
      "ruleName": "ttp_powershell_decodebase64_ns139797",
```


## List Search Queries

### Help for `chronicle search list-search-queries`
```
❯ chronicle search list-search-queries --help
Usage: chronicle search list-search-queries [OPTIONS]

  List search queries for a specific user.

Options:
  --user-id TEXT       ID of the user whose search queries to list.
                       [required]
  --page-size INTEGER  Optional maximum number of search queries to return.
  --page-token TEXT    Optional page token from a previous response.
  --help               Show this message and exit.

```

### Example Usage for `chronicle search list-search-queries`
```
chronicle search list-search-queries \
  --user-id "admin@dandye.altostrat.com" \
  --page-size 100
```