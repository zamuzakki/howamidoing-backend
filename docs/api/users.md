# Users
Supports registering, viewing, and updating anonymous user for report creation.

## Register a new user

**Request**:

`POST` `/users/`

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
201 Created

{
  "id": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011"
}
```

The `id` returned with this response should be stored by the client for creating report.


## Get a user

**Request**:

`GET` `/users/:id`

URL Parameters:
- id: ID of the user

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011"
}
```