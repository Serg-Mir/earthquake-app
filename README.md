# Earthquake Detection and Storage Application

## Overview
This Python application fetches earthquake data from the USGS API, filters results based on proximity to Pleo's offices by default, and stores the data in Google BigQuery.

## Features:
- Fetch earthquake data from the USGS API.
- Filter by proximity to Pleo office locations.
- Store earthquake data in Google BigQuery.
- Custom input support for location, period and radius

## Local installation:

1. Clone the repository:
    ```
    git clone git@github.com:Serg-Mir/earthquake-app.git
    cd earthquake-app
    ```

2. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the app:
    ```
    python earthquake_app/main.py
    ```

## Docker setup

Make sure you have [Docker](https://docs.docker.com) installed in your local machine.

Create a Docker image from the Earthquake App project:

```bash
DOCKER_BUILDKIT=1 docker build \
  --ssh default \
  --tag earthquake-app \
  .
```

**Note:** If you are using MacOS, you may need to run `ssh-add` to add private key identities to the
authentication agent first for this to work.

You can run the Docker container in local once the image is built:

```bash
docker run --env-file .env --env GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials/file.json" earthquake-app <ARGUMENTS>
```
## Testing
1. You might need to add the generated project root directory to the
[`PYTHONPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH) in some cases: `export PYTHONPATH="{$PYTHONPATH}:/absolute/path/to/project"`
2. Run `pytest tests/` (_not implemented yet_)

## Usage examples:
### Default values(pre-defined known offices locations)
```
$ python earthquake_app/main.py
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:13] Earthquake data found for 2 km WSW of Marans, France
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:16] Successfully stored in BigQuery.
---
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:13] Earthquake data found for 5 km S of Rudna, Poland
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:16] Successfully stored in BigQuery.
---
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:13] Earthquake data found for Azores-Cape St. Vincent Ridge
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:16] Successfully stored in BigQuery.
---
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:13] Earthquake data found for 4 km S of Lanjarón, Spain
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:16] Successfully stored in BigQuery.
---
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:13] Earthquake data found for 2 km SE of Cheadle, United Kingdom
INFO: [earthquake_app.process:fetch_earthquakes_near_offices:16] Successfully stored in BigQuery.
---
```
### Custom coordinates and radius
```
$ python earthquake_app/main.py --lat 13.006395484423336 --lon 42.734473054904896 --radius 650
INFO: [earthquake_app.process:fetch_earthquakes_custom_zone:22] Earthquake data found for 154 km NNW of Las Khorey, Somalia
INFO: [earthquake_app.utils:store_in_bigquery:43] Data stored successfully.
---
```
### Using pre-built docker container
```
$ docker run --env GOOGLE_APPLICATION_CREDENTIALS=earthquake-data-436210-a18aafd4ce1e.json earthquake-app --lat 35 --lon 44 --radius 660
INFO: [earthquake_app.process:fetch_earthquakes_custom_zone:22] Earthquake data found for 8 km N of Doğanyol, Turkey
INFO: [earthquake_app.utils:store_in_bigquery:43] Data stored successfully.
---

```