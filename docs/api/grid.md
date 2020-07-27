# Grid
Supports creating, viewing, listing, updating, and deleting grid.
Some implementation might be unused by the howamidoing-frontend, e.g. creating/deleting/updating grid.

## Get a grid information

**Request**:

`GET` `/api/v1/grid/:id/`

URL Parameters:
- id: ID of the grid


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