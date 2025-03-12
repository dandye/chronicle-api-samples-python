# Detect Examples

## Detect Help
```
❯ chronicle detect --help
Usage: chronicle detect [OPTIONS] COMMAND [ARGS]...

  Detection API commands.

Options:
  --help  Show this message and exit.

Commands:
  alerts      Alert management commands.
  detections  Detection management commands.
  errors      Error management commands.
  retrohunts  Retrohunt management commands.
  rules       Rule management commands.
  rulesets    Rule set deployment commands.

```

## Alerts

### Help for `chronicle detect alerts`
```
❯ chronicle detect alerts --help
Usage: chronicle detect alerts [OPTIONS] COMMAND [ARGS]...

  Alert management commands.

Options:
  --help  Show this message and exit.

Commands:
  get     Get an alert by ID.
  update  Update an existing alert.

```

### Example Usage for `chronicle detect alerts get`
```
❯ chronicle detect alerts get \
  --alert-id "al_123e4567-e89b-12d3-a456-426614174000"
{
  "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/alerts/al_123e4567-e89b-12d3-a456-426614174000",
  "alertState": "ALERTING",
  "createTime": "2025-03-12T14:00:00Z",
  "detections": [
    "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/detections/de_92092e71-3baa-0ebf-f230-4aacc5952c63"
  ]
}
```

## Detections

### Help for `chronicle detect detections`
```
❯ chronicle detect detections --help
Usage: chronicle detect detections [OPTIONS] COMMAND [ARGS]...

  Detection management commands.

Options:
  --help  Show this message and exit.

Commands:
  get   Get a detection by ID.
  list  List detections.

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
      "ruleId": "ru_bf30236c-13af-4a85-a3af-5d58205e10f0",
      "detectionTime": "2025-03-12T14:30:00Z",
      "detectionFields": {
        "principal.hostname": "workstation-001",
        "principal.ip": "10.0.0.5",
        "target.ip": "198.51.100.5"
      }
    }
  ]
}
```

### Example Usage for `chronicle detect detections list`
```
❯ chronicle detect detections list \
  --filter "createTime > \"2025-03-10T00:00:00Z\"" \
  --page-size 10
{
  "detections": [
    {
      "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/detections/de_92092e71-3baa-0ebf-f230-4aacc5952c63",
      "type": "RULE_DETECTION",
      "createTime": "2025-03-12T14:30:00Z",
      "alertState": "ALERTING",
      "ruleName": "ttp_powershell_decodebase64_ns139797",
      "ruleId": "ru_bf30236c-13af-4a85-a3af-5d58205e10f0"
    }
  ],
  "nextPageToken": "next_page_token_value"
}
```

## Rules

### Help for `chronicle detect rules`
```
❯ chronicle detect rules --help
Usage: chronicle detect rules [OPTIONS] COMMAND [ARGS]...

  Rule management commands.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new rule.
  delete  Delete a rule.
  enable  Enable a rule.
  get     Get a rule by ID.
  list    List rules.

```

### Example Usage for `chronicle detect rules get`
```
❯ chronicle detect rules get \
  --rule-id "ru_bf30236c-13af-4a85-a3af-5d58205e10f0"
{
  "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/rules/ru_bf30236c-13af-4a85-a3af-5d58205e10f0",
  "type": "RULE",
  "ruleName": "ttp_powershell_decodebase64_ns139797",
  "ruleText": "rule ttp_powershell_decodebase64_ns139797 {
  meta:
    author = "Chronicle Security"
    description = "Identifies the use of ConvertTo-SecureString cmdlet with -Key parameter in PowerShell."
    severity = "MEDIUM"
    rule_name = "ttp_powershell_decodebase64_ns139797"

  events:
    $process.metadata.event_type = "PROCESS_LAUNCH"
    $process.target.process.command_line = /.*ConvertTo-SecureString.+\\s+-key.*/i

  match:
    $process over 1h

  outcome:
    $risk_score = max(75)
    $mitre_attack_tactic = "Defense Evasion"
    $mitre_attack_technique = "Obfuscated Files or Information: Deobfuscate/Decode Files or Information"
    $mitre_attack_technique_id = "T1140"
}",
  "versionId": "ver_123e4567-e89b-12d3-a456-426614174000",
  "compilationState": "SUCCEEDED",
  "enabledTime": "2025-03-01T12:00:00Z",
  "liveTime": "2025-03-01T12:05:00Z"
}
```

## Retrohunts

### Help for `chronicle detect retrohunts`
```
❯ chronicle detect retrohunts --help
Usage: chronicle detect retrohunts [OPTIONS] COMMAND [ARGS]...

  Retrohunt management commands.

Options:
  --help  Show this message and exit.

Commands:
  create  Create a new retrohunt.
  get     Get a retrohunt by ID.

```

### Example Usage for `chronicle detect retrohunts create`
```
❯ chronicle detect retrohunts create \
  --json-body '{"rule": {"ruleName": "my_retrohunt_rule", "ruleText": "rule my_retrohunt_rule {\n  meta:\n    author = \"Security Team\"\n    description = \"Test retrohunt rule\"\n  events:\n    $e.metadata.event_type = \"NETWORK_CONNECTION\"\n    $e.target.ip = \"198.51.100.5\"\n  match:\n    $e over 5m\n  outcome:\n    $risk_score = max(50)\n}"},"windowStartTime": "2025-02-01T00:00:00Z","windowEndTime": "2025-03-01T00:00:00Z"}'
{
  "name": "projects/my-project/locations/us/instances/3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d/retrohunts/rh_123e4567-e89b-12d3-a456-426614174000",
  "createTime": "2025-03-12T15:00:00Z",
  "state": "RUNNING",
  "rule": {
    "ruleName": "my_retrohunt_rule",
    "ruleText": "rule my_retrohunt_rule {\n  meta:\n    author = \"Security Team\"\n    description = \"Test retrohunt rule\"\n  events:\n    $e.metadata.event_type = \"NETWORK_CONNECTION\"\n    $e.target.ip = \"198.51.100.5\"\n  match:\n    $e over 5m\n  outcome:\n    $risk_score = max(50)\n}"
  },
  "windowStartTime": "2025-02-01T00:00:00Z",
  "windowEndTime": "2025-03-01T00:00:00Z"
}
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
❯ PROJECT_INSTANCE=3a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d
PROJECT_ID=my-project
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
      "ruleId": "ru_bf30236c-13af-4a85-a3af-5d58205e10f0",
      "detectionTime": "2025-03-12T14:30:00Z",
      "detectionFields": {
        "principal.hostname": "workstation-001",
        "principal.ip": "10.0.0.5",
        "target.ip": "198.51.100.5"
      }
    }
  ]
}
```