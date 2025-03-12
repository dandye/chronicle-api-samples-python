# IoCs Examples

## IoCs Help
```
❯ chronicle iocs --help
Usage: chronicle iocs [OPTIONS] COMMAND [ARGS]...

  IoCs API commands.

Options:
  --help  Show this message and exit.

Commands:
  batch-get  Get multiple IoCs by their values.
  get        Get an IoC by its value.
  get-state  Get the state of an IoC by its value.

```

## Get IoC

### Help for `chronicle iocs get`
```
❯ chronicle iocs get --help
Usage: chronicle iocs get [OPTIONS]

  Get an IoC by its value.

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
  --ioc-value TEXT         Value of the IoC to retrieve.  [required]
  --ioc-type TEXT          Type of IoC being requested.  [required]
  --help                   Show this message and exit.
```

### Example Usage for `chronicle iocs get`
```
❯ chronicle iocs get \
  --ioc-value "malware.com" \
  --ioc-type "DOMAIN"
{
  "ioc": {
    "value": "malware.com",
    "type": "DOMAIN",
    "firstSeenTime": "2025-02-01T12:00:00Z",
    "lastSeenTime": "2025-03-12T14:00:00Z",
    "sources": [
      {
        "source": "THREAT_INTEL_FEED",
        "confidence": 80,
        "category": "MALWARE_DOMAIN"
      }
    ],
    "severity": "HIGH",
    "state": "ACTIVE"
  }
}
```

## Batch Get IoCs

### Help for `chronicle iocs batch-get`
```
❯ chronicle iocs batch-get --help
Usage: chronicle iocs batch-get [OPTIONS]

  Get multiple IoCs by their values.

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
  --ioc-values TEXT        JSON array of IoC values to retrieve.  [required]
  --ioc-type [IOC_TYPE_UNSPECIFIED|DOMAIN|IP|FILE_HASH|URL|USER_EMAIL|MUTEX|FILE_HASH_MD5|FILE_HASH_SHA1|FILE_HASH_SHA256|IOC_TYPE_RESOURCE]
                           Type of IoCs being requested.  [required]
  --help                   Show this message and exit.
```

### Example Usage for `chronicle iocs batch-get`
```
❯ chronicle iocs batch-get \
  --ioc-values '["malware.com", "evil.com"]' \
  --ioc-type "DOMAIN"
{
  "iocs": [
    {
      "value": "malware.com",
      "type": "DOMAIN",
      "firstSeenTime": "2025-02-01T12:00:00Z",
      "lastSeenTime": "2025-03-12T14:00:00Z",
      "sources": [
        {
          "source": "THREAT_INTEL_FEED",
          "confidence": 80,
          "category": "MALWARE_DOMAIN"
        }
      ],
      "severity": "HIGH",
      "state": "ACTIVE"
    },
    {
      "value": "evil.com",
      "type": "DOMAIN",
      "firstSeenTime": "2025-01-15T09:30:00Z",
      "lastSeenTime": "2025-03-10T16:45:00Z",
      "sources": [
        {
          "source": "THREAT_INTEL_FEED",
          "confidence": 90,
          "category": "C2_DOMAIN"
        }
      ],
      "severity": "CRITICAL",
      "state": "ACTIVE"
    }
  ]
}
```

## Get IoC State

### Help for `chronicle iocs get-state`
```
❯ chronicle iocs get-state --help
Usage: chronicle iocs get-state [OPTIONS]

  Get the state of an IoC by its value.

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
  --ioc-value TEXT         Value of the IoC to retrieve state for.  [required]
  --ioc-type TEXT          Type of IoC being requested.  [required]
  --help                   Show this message and exit.
```

### Example Usage for `chronicle iocs get-state`
```
❯ chronicle iocs get-state \
  --ioc-value "malware.com" \
  --ioc-type "DOMAIN"
{
  "state": "ACTIVE",
  "firstSeenTime": "2025-02-01T12:00:00Z",
  "lastSeenTime": "2025-03-12T14:00:00Z"
}
```

### Example Usage for `-m iocs.v1alpha.get_ioc`
```
❯ python3 -m iocs.v1alpha.get_ioc --help
usage: get_ioc.py [-h] [-c CREDENTIALS_FILE] -i PROJECT_INSTANCE -p PROJECT_ID
                  [-r {asia-northeast1,asia-south1,asia-southeast1,australia-southeast1,eu,europe,europe-west12,europe-west2,europe-west3,europe-west6,europe-west9,me-central1,me-central2,me-west1,northamerica-northeast2,southamerica-east1,us}]
                  --ioc_value IOC_VALUE --ioc_type
                  {IOC_TYPE_UNSPECIFIED,DOMAIN,IP,FILE_HASH,URL,USER_EMAIL,MUTEX,FILE_HASH_MD5,FILE_HASH_SHA1,FILE_HASH_SHA256,IOC_TYPE_RESOURCE}

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
  --ioc_value IOC_VALUE
                        Value of the IoC to retrieve
  --ioc_type {IOC_TYPE_UNSPECIFIED,DOMAIN,IP,FILE_HASH,URL,USER_EMAIL,MUTEX,FILE_HASH_MD5,FILE_HASH_SHA1,FILE_HASH_SHA256,IOC_TYPE_RESOURCE}
                        Type of IoC being requested
```

```
❯ PROJECT_INSTANCE=3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d
PROJECT_ID=my-project
python3 -m iocs.v1alpha.get_ioc \
 --project_instance=$PROJECT_INSTANCE  \
 --project_id=$PROJECT_ID \
 --ioc_value "malware.com" \
 --ioc_type "DOMAIN"
{
  "ioc": {
    "value": "malware.com",
    "type": "DOMAIN",
    "firstSeenTime": "2025-02-01T12:00:00Z",
    "lastSeenTime": "2025-03-12T14:00:00Z",
    "sources": [
      {
        "source": "THREAT_INTEL_FEED",
        "confidence": 80,
        "category": "MALWARE_DOMAIN"
      }
    ],
    "severity": "HIGH",
    "state": "ACTIVE"
  }
}
```