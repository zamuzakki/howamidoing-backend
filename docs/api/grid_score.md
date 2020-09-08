# GridScore
Supports viewing and listing grid-score score.


## List GridScore as vector tile

**Request**:

`GET` `/v2/api/grid-score-tiles/?tile=:z/:x/:y`

Query Parameters:
- zoom: Zoom level of the map
- x: x value of the map
- y: y value of the map

Those values are usually generated automatically by the map (OpenLayer or Leaflet)

**Response**:

```
Content-Type application/vnd.mapbox-vector-tile
200 OK
```

If the z, x, and y does not have any GridScore, it will return
```
Content-Type application/vnd.mapbox-vector-tile
204 OK
b""
```