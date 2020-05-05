# GridScore
Supports viewing and listing grid-score score.


## Get a grid-score information

**Request**:

`GET` `/api/v1/grid-score/:id/`

URL Parameters:
- id: ID of the grid-score

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": 554,
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          18.485019801338506,
          -33.96681873937577
        ],
        [
          18.494002954179702,
          -33.96681873937577
        ],
        [
          18.494002954179702,
          -33.97426869213914
        ],
        [
          18.485019801338506,
          -33.97426869213914
        ],
        [
          18.485019801338506,
          -33.96681873937577
        ]
      ]
    ]
  },
  "properties": {
    "score_green": "0.00",
    "count_green": 0,
    "score_yellow": "0.00",
    "count_yellow": 0,
    "score_red": "0.00",
    "count_red": 1,
    "population": 90,
    "total_report": 1,
    "total_score": "1.00"
  }
}
```


## List grid-score

**Request**:

`GET` `/api/v1/grid-score/`

Query Parameters:
Name              | Type    | Description
------------------|---------|----------------------------------------------
page              | integer | Page number within the paginated result set
max_population    | integer | Minimum number of population in the grid-score
min_population    | integer | Maximum number of population in the grid-score
max_total_report  | integer | Maximum number of report in the grid-score
min_total_report  | integer | Minimum number of report in the grid-score
total_score       | integer | Total score the grid-score (0=green, 1=yellow, 2=red)
contains_geom     | string  | GeoJSON Geometry string representing geometry inside the grid-score


*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": 554,
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          18.485019801338506,
          -33.96681873937577
        ],
        [
          18.494002954179702,
          -33.96681873937577
        ],
        [
          18.494002954179702,
          -33.97426869213914
        ],
        [
          18.485019801338506,
          -33.97426869213914
        ],
        [
          18.485019801338506,
          -33.96681873937577
        ]
      ]
    ]
  },
  "properties": {
    "score_green": "0.00",
    "count_green": 0,
    "score_yellow": "0.00",
    "count_yellow": 0,
    "score_red": "0.00",
    "count_red": 1,
    "population": 90,
    "total_report": 1,
    "total_score": "1.00"
  }
}
```
