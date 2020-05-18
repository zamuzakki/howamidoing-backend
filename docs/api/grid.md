# Grid
Supports creating, viewing, listing, updating, and deleting grid.
Some implementation might be unused by the howamidoing-frontend, e.g. creating/deleting/updating grid.

## Create a new grid

**Request**:

`POST` `/api/v1/grid/`

Payload Parameters:

Name        | Type    | Required  | Description
------------|---------|-----------|------------
geometry    | string  | Yes       | The GeoJSON Polygon Geometry string for the new grid.
population  | integer | Yes       | The number of population for the new grid.

*Note:*

- **[Authorization Protected, Admin Only](authentication.md)**

**Response**:

```json
Content-Type application/json
201 Created

{
    "id": 1490,
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    18.727564928050775,
                    -34.06361719515123
                ],
                [
                    18.73654808089197,
                    -34.06361719515123
                ],
                [
                    18.73654808089197,
                    -34.07105865748019
                ],
                [
                    18.727564928050775,
                    -34.07105865748019
                ],
                [
                    18.727564928050775,
                    -34.06361719515123
                ]
            ]
        ]
    },
    "properties": {
        "population": 90
    }
}
```


## Get a grid information

**Request**:

`GET` `/api/v1/grid/:id/`

URL Parameters:
- id: ID of the grid

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "id": 1490,
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    18.727564928050775,
                    -34.06361719515123
                ],
                [
                    18.73654808089197,
                    -34.06361719515123
                ],
                [
                    18.73654808089197,
                    -34.07105865748019
                ],
                [
                    18.727564928050775,
                    -34.07105865748019
                ],
                [
                    18.727564928050775,
                    -34.06361719515123
                ]
            ]
        ]
    },
    "properties": {
        "population": 90
    }
}
```


## List grid

**Request**:

`GET` `/api/v1/grid/`

Query Parameters:
Name            | Type    | Description
----------------|---------|----------------------------------------------
page            | integer | Page number within the paginated result set
max_population  | integer | Minimum number of population in the grid
min_population  | integer | Maximum number of population in the grid
contains_geom   | string  | GeoJSON Geometry string representing geometry inside the grid


*Note:*

- **[Authorization Protected](authentication.md)**

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
            "id": 1490,
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            18.727564928050775,
                            -34.06361719515123
                        ],
                        [
                            18.73654808089197,
                            -34.06361719515123
                        ],
                        [
                            18.73654808089197,
                            -34.07105865748019
                        ],
                        [
                            18.727564928050775,
                            -34.07105865748019
                        ],
                        [
                            18.727564928050775,
                            -34.06361719515123
                        ]
                    ]
                ]
            },
            "properties": {
                "population": 90
            }
        }
    ]
  }
}
```


## Update a grid

**Request**:

`PUT/PATCH` `/api/v1/grid/:id/`

URL Parameters:
- id: ID of the grid

Data Parameters:

Name        | Type    | Required  | Description
------------|---------|-----------|------------
geometry    | string  | Yes       | The GeoJSON Polygon Geometry string coordinate.
population  | integer | Yes       | The number of population.

*Note:*

- The fields are required for PUT or update, optional for PATCH or partial update

- **[Authorization Protected, Admin/Owner Only](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "id": 1490,
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    18.727564928050775,
                    -34.06361719515123
                ],
                [
                    18.73654808089197,
                    -34.06361719515123
                ],
                [
                    18.73654808089197,
                    -34.07105865748019
                ],
                [
                    18.727564928050775,
                    -34.07105865748019
                ],
                [
                    18.727564928050775,
                    -34.06361719515123
                ]
            ]
        ]
    },
    "properties": {
        "population": 99
    }
}
```


## Delete a grid

**Request**:

`DELETE` `/api/v1/grid/:id/`

Parameters:
- id: ID of the grid

*Note:*

- **[Authorization Protected, Admin/Owner Only](authentication.md)**

**Response**:

```json
Content-Type application/json
204 OK
```
