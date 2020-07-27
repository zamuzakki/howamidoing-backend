# Status
Supports creating, viewing, listing, updating, and deleting status.


## Get a status information

**Request**:

`GET` `/api/v1/status/:id/`

URL Parameters:
- id: ID of the status

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