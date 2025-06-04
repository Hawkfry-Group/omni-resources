# Omni Logs Structure Documentation

## Directory Structure
The logs are organized in a hierarchical time-based structure:

```
omni_logs/
└── YYYY/                  # Year
    └── MM/               # Month (01-12)
        └── DD/          # Day (01-31)
            └── HH/      # Hour (00-23)
                └── [log files]
```

## Log File Naming Convention
Files follow the pattern:
```
{Region}-{Service}-{Version}-{DateTime}-{UUID}-{OrganizationID}
```

Example:
```
EastUsa-Firehose-2-2025-03-07-16-35-07-74b72b94-3961-4d29-bb0e-e1c47d651c9a-b25a5ced-5b33-47af-bd5d-588241abe962
```

## Log Content Structure
Logs are stored in JSON format with the following key information:

### Common Fields
- `@timestamp`: ISO 8601 timestamp
- `log.level`: Logging level (INFO, etc.)
- `organizationId`: Unique identifier for the organization
- `userId`: Unique identifier for the user
- `traceId`: Request tracking ID

### Event Types
1. **QUERY_CONTEXT**
   - Captures query context information
   - Contains referrer and URL information
   - Includes query count and document identifiers

2. **QUERY_EXECUTE**
   - Records query execution details
   - Includes duration and query text
   - Contains job and stage IDs

### Infrastructure Information
- **Platform**: AWS ECS (Elastic Container Service)
- **Region**: East USA
- **Services**:
  - `omni-app-remix`
  - `omni-modelworkerservice`
- **Container Details**:
  - Container ID
  - Container name
  - ECS cluster
  - Task ARN
  - Task definition

## Log Schema
Below is the complete schema for log entries:

### Base Fields (All Events)
```json
{
    "@timestamp": "string (ISO 8601)",
    "ecs.version": "string",
    "log.level": "string (INFO, etc.)",
    "process.thread.name": "string",
    "log.logger": "string",
    "marker": "string (e.g., 'AUDIT')",
    "organizationId": "string (UUID)",
    "userId": "string (UUID)",
    "traceId": "string",
    "container_id": "string",
    "container_name": "string",
    "source": "string (e.g., 'stdout')",
    "ecs_cluster": "string",
    "ecs_task_arn": "string",
    "ecs_task_definition": "string"
}
```

### QUERY_CONTEXT Event
```json
{
    // ... base fields ...
    "event": "QUERY_CONTEXT",
    "documentIdentifier": "string",
    "embedEntity": "null | object",
    "queryCount": "string",
    "referrer": "string (URL path)",
    "url": "string (full URL)",
    "trace_flags": "string"
}
```

### QUERY_EXECUTE Event
```json
{
    // ... base fields ...
    "event": "QUERY_EXECUTE",
    "duration": "string (milliseconds)",
    "jobId": "string (UUID)",
    "message": "string",
    "omniQueryId": "string (UUID)",
    "query": "string (SQL query)",
    "requestId": "string (UUID)",
    "span_id": "string",
    "stageId": "string (UUID)",
    "trace_flags": "string",
    "trace_id": "string"
}
```

### Container-Specific Fields
```json
{
    "container_id": "string (e.g., '2833693fb5e740edb342f430840a934b-3046001938')",
    "container_name": "string (e.g., 'omni-app-remix', 'omni-modelworkerservice')",
    "ecs_cluster": "string (e.g., 'EastUsa')",
    "ecs_task_arn": "string (AWS ARN)",
    "ecs_task_definition": "string (e.g., 'EastUsaRemixTaskDef7EC65A23:8259')"
}
```

## Query Matching Between Omni and BigQuery
The `omniQueryId` in the QUERY_EXECUTE events serves as a crucial linking key between Omni logs and BigQuery's INFORMATION_SCHEMA logs. This enables tracking queries from user interaction through to execution in BigQuery.

### Matching Queries
To match Omni queries with their corresponding BigQuery execution, use the following query pattern:

```sql
query to pull two specific queries from bigquery information schema logging which match to omni logs
SELECT
    start_time,
    creation_time,
    label.key AS label_key,
    label.value AS label_value,
    query
FROM `region-eu`.INFORMATION_SCHEMA.JOBS_BY_PROJECT, 
UNNEST(labels) AS label
WHERE label.value IN ('omniQueryId1', 'omniQueryId2')
ORDER BY start_time DESC;
```

This correlation allows you to:
- Track query execution across systems
- Match BigQuery queries back to specific Omni users
- Audit query patterns and performance
- Monitor user activity and resource usage

Example: An `omniQueryId` like "77b1ea39-ca99-42c6-9d90-fb97c3e93490" in Omni logs can be used to find the exact query execution details in BigQuery's INFORMATION_SCHEMA.

## Example Log Entry
```json
{
    "@timestamp": "2025-03-07T16:35:13.409Z",
    "ecs.version": "1.2.0",
    "log.level": "INFO",
    "event": "QUERY_EXECUTE",
    "organizationId": "b25a5ced-5b33-47af-bd5d-588241abe962",
    "userId": "2424e5f2-521f-4f96-978f-b9625d58e5ef",
    "duration": "88",
    "container_name": "omni-modelworkerservice",
    "ecs_cluster": "EastUsa"
}
```

## Usage Notes
- Logs are organized chronologically for easy retrieval
- Each hour has its own directory for efficient log rotation
- JSON format enables easy parsing and analysis
- Comprehensive tracing system implemented through trace IDs
- Full audit logging capabilities for query execution
