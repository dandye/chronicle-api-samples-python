# Ingestion Examples

## Ingestion Help
```
❯ chronicle ingestion --help
Usage: chronicle ingestion [OPTIONS] COMMAND [ARGS]...

  Ingestion API commands.

Options:
  --help  Show this message and exit.

Commands:
  batch-get-events  Batch get events by IDs.
  get-event         Get event details by ID.
  import-events     Import events into Chronicle.

```

## Import Events

### Help for `chronicle ingestion import-events`
```
❯ chronicle ingestion import-events --help
Usage: chronicle ingestion import-events [OPTIONS]

  Import events into Chronicle.

Options:
  --json-events TEXT  Events in (serialized) JSON format.  [required]
  --help              Show this message and exit.
```

### Example Usage for `chronicle ingestion import-events`
```
❯ chronicle ingestion import-events \
  --json-events '{"events": [{"metadata": {"eventTimestamp": "2025-03-12T14:00:00Z", "eventType": "NETWORK_CONNECTION", "productName": "Sample Product", "vendorName": "Sample Vendor"}, "network": {"applicationProtocol": "HTTPS", "direction": "OUTBOUND", "ipProtocol": "TCP", "sourceIp": "10.0.0.1", "sourcePort": 12345, "destinationIp": "198.51.100.1", "destinationPort": 443}}]}'
{
  "events": [
    {
      "id": "evt_123e4567-e89b-12d3-a456-426614174000",
      "status": "ACCEPTED"
    }
  ]
}
```

## Get Event

### Help for `chronicle ingestion get-event`
```
❯ chronicle ingestion get-event --help
Usage: chronicle ingestion get-event [OPTIONS]

  Get event details by ID.

Options:
  --event-id TEXT  The ID of the event to retrieve.  [required]
  --help           Show this message and exit.
```

### Example Usage for `chronicle ingestion get-event`
```
❯ chronicle ingestion get-event \
  --event-id "evt_123e4567-e89b-12d3-a456-426614174000"
{
  "eventId": "evt_123e4567-e89b-12d3-a456-426614174000",
  "status": "PROCESSED",
  "metadata": {
    "eventTimestamp": "2025-03-12T14:00:00Z",
    "eventType": "NETWORK_CONNECTION",
    "productName": "Sample Product",
    "vendorName": "Sample Vendor"
  },
  "network": {
    "applicationProtocol": "HTTPS",
    "direction": "OUTBOUND",
    "ipProtocol": "TCP",
    "sourceIp": "10.0.0.1",
    "sourcePort": 12345,
    "destinationIp": "198.51.100.1",
    "destinationPort": 443
  }
}
```

## Batch Get Events

### Help for `chronicle ingestion batch-get-events`
```
❯ chronicle ingestion batch-get-events --help
Usage: chronicle ingestion batch-get-events [OPTIONS]

  Batch get events by IDs.

Options:
  --event-ids TEXT  JSON string containing a list of event IDs to retrieve.
                     [required]
  --help            Show this message and exit.
```

### Example Usage for `chronicle ingestion batch-get-events`
```
❯ chronicle ingestion batch-get-events \
  --event-ids '["evt_123e4567-e89b-12d3-a456-426614174000", "evt_123e4567-e89b-12d3-a456-426614174001"]'
{
  "events": [
    {
      "eventId": "evt_123e4567-e89b-12d3-a456-426614174000",
      "status": "PROCESSED",
      "metadata": {
        "eventTimestamp": "2025-03-12T14:00:00Z",
        "eventType": "NETWORK_CONNECTION",
        "productName": "Sample Product",
        "vendorName": "Sample Vendor"
      },
      "network": {
        "applicationProtocol": "HTTPS",
        "direction": "OUTBOUND",
        "ipProtocol": "TCP",
        "sourceIp": "10.0.0.1",
        "sourcePort": 12345,
        "destinationIp": "198.51.100.1",
        "destinationPort": 443
      }
    },
    {
      "eventId": "evt_123e4567-e89b-12d3-a456-426614174001",
      "status": "PROCESSED",
      "metadata": {
        "eventTimestamp": "2025-03-12T14:30:00Z",
        "eventType": "NETWORK_CONNECTION",
        "productName": "Sample Product",
        "vendorName": "Sample Vendor"
      },
      "network": {
        "applicationProtocol": "HTTP",
        "direction": "INBOUND",
        "ipProtocol": "TCP",
        "sourceIp": "192.0.2.1",
        "sourcePort": 54321,
        "destinationIp": "10.0.0.1",
        "destinationPort": 80
      }
    }
  ]
}
```

### Example Usage for `-m ingestion.v1alpha.events_batch_get`
```
❯ python3 -m ingestion.v1alpha.events_batch_get --help
usage: events_batch_get.py [-h] [-c CREDENTIALS_FILE] -i PROJECT_INSTANCE -p PROJECT_ID
                           [-r {asia-northeast1,asia-south1,asia-southeast1,australia-southeast1,eu,europe,europe-west12,europe-west2,europe-west3,europe-west6,europe-west9,me-central1,me-central2,me-west1,northamerica-northeast2,southamerica-east1,us}]
                           --event_ids EVENT_IDS

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
  --event_ids EVENT_IDS
                        JSON string containing a list of event IDs to retrieve
```

```
❯ PROJECT_INSTANCE=3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d
PROJECT_ID=my-project
python3 -m ingestion.v1alpha.events_batch_get \
 --project_instance=$PROJECT_INSTANCE  \
 --project_id=$PROJECT_ID \
 --event_ids '["evt_123e4567-e89b-12d3-a456-426614174000", "evt_123e4567-e89b-12d3-a456-426614174001"]'
{
  "events": [
    {
      "eventId": "evt_123e4567-e89b-12d3-a456-426614174000",
      "status": "PROCESSED",
      "metadata": {
        "eventTimestamp": "2025-03-12T14:00:00Z",
        "eventType": "NETWORK_CONNECTION",
        "productName": "Sample Product",
        "vendorName": "Sample Vendor"
      },
      "network": {
        "applicationProtocol": "HTTPS",
        "direction": "OUTBOUND",
        "ipProtocol": "TCP",
        "sourceIp": "10.0.0.1",
        "sourcePort": 12345,
        "destinationIp": "198.51.100.1",
        "destinationPort": 443
      }
    },
    {
      "eventId": "evt_123e4567-e89b-12d3-a456-426614174001",
      "status": "PROCESSED",
      "metadata": {
        "eventTimestamp": "2025-03-12T14:30:00Z",
        "eventType": "NETWORK_CONNECTION",
        "productName": "Sample Product",
        "vendorName": "Sample Vendor"
      },
      "network": {
        "applicationProtocol": "HTTP",
        "direction": "INBOUND",
        "ipProtocol": "TCP",
        "sourceIp": "192.0.2.1",
        "sourcePort": 54321,
        "destinationIp": "10.0.0.1",
        "destinationPort": 80
      }
    }
  ]
}
```