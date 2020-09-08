# Grid Setup
This document will explain KmGrid setup,so you can have grid with population data in it.


## For instance running without Docker
1. Activate your Python environment

2. Use this command to import:
```
$ cd howamidoing-backend/
$ python manage.py import_grid --file /path/to/grid/file/grid_file.geojson
$ python manage.py generate_grid_score --select=non-existing
```


## For instance running using Docker

1. Copy your GEOJson file to `/deployment/backups/`.

2. Use the following command.
```
$ make shell
$ python manage.py import_grid --file backups/your_grid_file.geojson
$ python manage.py generate_grid_score --select=non-existing
```


The GEOJson file must use WGS84-EPSG:3857 as CRS. You can check the GEOJson file example [here](https://github.com/kartoza/howamidoing-backend/blob/develop/example/grid.geojson)