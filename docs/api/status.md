# Status
Supports creating, viewing, listing, updating, and deleting status.

## Create a new status

**Request**:

`POST` `/api/v1/status/`

Payload Parameter:

Name          | Type   | Required | Description
--------------|--------|----------|------------
name          | string | Yes      | The name for the new status.
description   | string | No       | The description for the new status.

*Note:*

- **[Authorization Protected, Admin Only](authentication.md)**

**Response**:

```json
Content-Type application/json
201 Created

{
  "id": 1,
  "name": "All is well here",
  "description": "Everything is good."
}
```


## Get a status information

**Request**:

`GET` `/api/v1/status/:id/`

URL Parameters:
- id: ID of the status

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": 1,
  "name": "All is well here",
  "description": "Everything is good."
}
```


## List status

**Request**:

`GET` `/api/v1/status/?page={page}`

Query Parameters:
- page: A page number within the paginated result set.

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "name": "All is well",
      "description": "Everything is good."
    },
    {
      "id": 2,
      "name": "Need Medical Help",
      "description": "Need Medical Help."
    }
  ]
}
```


## Update a status

**Request**:

`PUT/PATCH` `/api/v1/status/:id/`

URL Parameters:
- id: ID of the status

Payload Parameters:
Name          | Type   | Required | Description
--------------|--------|----------|------------
name          | string | Yes      | The name for the new status.
description   | string | No       | The description for the new status.

*Note:*

- **[Authorization Protected, Admin Only](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": 1,
  "name": "All is well here",
  "description": "Everything is good. Food is sufficient, health is prime, financially stable."
}
```


## Delete a status

**Request**:

`DELETE` `/api/v1/status/:id/`

Parameters:
- id: ID of the status

*Note:*

- **[Authorization Protected, Admin Only](authentication.md)**

**Response**:

```json
Content-Type application/json
204 OK
```
