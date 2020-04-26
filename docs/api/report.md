# Report
Supports creating, viewing, listing, updating, and deleting report.
Some implementation might be unused by the howamidoing-frontend, e.g. deleting/updating report.

## Create a new report

**Request**:

`POST` `/report/`

Parameters:

Name      | Type    | Required  | Description
----------|---------|-----------|------------
location  | string  | Yes       | The GeoJSON point string coordinate for the new report.
status    | integer | Yes       | The status ID for the new report.
user      | string  | Yes       | The user ID for the new report.

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
201 Created

{
  "id": 3,
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      -76.43941,
      39.33427
    ]
  },
  "properties": {
    "status": {
      "id": 2,
      "name": "Need Medical Help",
      "description": "Need Medical Help."
    },
    "user": {
      "id": "0b1a7d47-3f97-420b-9421-85c8d904c575",
      "username": "zulfi.muzakki",
      "first_name": "Zulfikar Akbar",
      "last_name": "Muzakki"
    },
    "timestamp": "2020-04-10T10:03:40+0000"
  }
}
```


## Get a report information

**Request**:

`GET` `/report/{id}`

Parameters:
- id: ID of the report

*Note:*

- **[Authorization Protected, Admin/Owner Only](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": 3,
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      -76.43941,
      39.33427
    ]
  },
  "properties": {
    "status": {
      "id": 2,
      "name": "Need Medical Help",
      "description": "Need Medical Help."
    },
    "user": {
      "id": "0b1a7d47-3f97-420b-9421-85c8d904c575",
      "username": "zulfi.muzakki",
      "first_name": "Zulfikar Akbar",
      "last_name": "Muzakki"
    },
    "timestamp": "2020-04-10T10:03:40+0000"
  }
}
```


## List report

**Request**:

`GET` `/report/?page={page}`

Parameters:
- page: A page number within the paginated result set.

*Note:*

- **[Authorization Protected, Admin Only](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "count": 1,
  "next": null,
  "previous": null,
  "results": {
    "type": "FeatureCollection",
    "features": [
      {
        "id": 3,
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [
            -76.43941,
            39.33427
          ]
        },
        "properties": {
          "status": {
            "id": 2,
            "name": "Need Medical Help",
            "description": "Need Medical Help"
          },
          "user": {
            "id": "0b1a7d47-3f97-420b-9421-85c8d904c575",
            "username": "zulfi.muzakki",
            "first_name": "Zulfikar Akbar",
            "last_name": "Muzakki"
          },
          "timestamp": "2020-04-10T10:03:40+0000"
        }
      }
    ]
  }
}
```


## Update a report

**Request**:

`PUT/PATCH` `/report/{id}`

Parameters:
- id: ID of the report

Parameters:

Name      | Type    | Required  | Description
----------|---------|-----------|------------
location  | string  | Yes       | The GeoJSON point string coordinate for the new report.
status    | integer | Yes       | The status ID for the new report.
user      | string  | Yes       | The user ID for the new report.

*Note:*

- **[Authorization Protected, Admin/Owner Only](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": 3,
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      -76.43941,
      39.33427
    ]
  },
  "properties": {
    "status": {
      "id": 3,
      "name": "All is well",
      "description": "Everything is good."
    },
    "user": {
      "id": "0b1a7d47-3f97-420b-9421-85c8d904c575",
      "username": "zulfi.muzakki",
      "first_name": "Zulfikar Akbar",
      "last_name": "Muzakki"
    },
    "timestamp": "2020-04-10T10:03:40+0000"
  }
}
```


## Delete a report

**Request**:

`DELETE` `/report/{id}`

Parameters:
- id: ID of the report

*Note:*

- **[Authorization Protected, Admin/Owner Only](authentication.md)**

**Response**:

```json
Content-Type application/json
204 OK
```
