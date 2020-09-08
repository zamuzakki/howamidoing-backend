# Report
Supports creating, viewing, and deleting report.

## Create a new report

**Request**:

`POST` `/v2/api/report/`

Payload Parameters:

Name      | Type    | Required  | Description
----------|---------|-----------|------------
location  | string  | Yes       | The GeoJSON Point Geometry string for the new report.
status    | integer | Yes       | The status ID for the new report.
user      | string  | Yes       | The user ID for the new report.

**Response**:

```json
Content-Type application/json
201 Created

{
  "id": 4,
  "status": {
    "id": 3,
    "name": "Need Medical Help",
    "description": ""
  },
  "timestamp": "2020-05-15T09:26:33+0000",
  "current": true,
  "grid": 288,
  "user": "ac3b9263-87a8-4198-9acb-ccb0c9a59c46"
}
```


## Delete a report

**Request**:

`DELETE` `/v2/api/report/:id/`

Parameters:
- id: ID of the report

**Response**:

```json
Content-Type application/json
204 No Content
```
