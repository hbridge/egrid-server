# egrid-server

Rest API for the EPA's [Emissions & Generation Resource Integrated Database](https://www.epa.gov/egrid)

Supports searching by Geolocation (latitude / longitude) via GeoDjango / PostGIS

Currently using 2020 data, new 2021 data was just released and will be supported soon

## Usage

1. `/api/plants` serves up a paginated list of all the plants in the database
1. `/api/plants/?lat=LAT&lng=LNG&rad=DIST` the plants endpoint supports query parameters for finding all plants within a radius of a latlong point

## Building

1. `pip install -r requirements.txt`

This app was built/tested with Python 3.11.1

## Running the server

This app was built to deploy to [Fly.io](https://fly.io/)

1. [Install PostGIS](https://postgis.net/install/) or run a [docker image](https://hub.docker.com/r/postgis/postgis) of it, taking note of any password you set on it.
    1. If you installed PostGIS, don't forget to run the `CREATE EXTENSION` [SQL statements]((https://postgis.net/install/)) on the database enable PostGIS
    1. If you're deploying to Fly.io, you'll need to connect to the database to run these extensions
1. Set Environmental Variables
    1. `EGRID_SERVER_DJANGO_SECRET_KEY` – used by Django to encrypt session keys
    1. `DATABASE_URL` – used by Django to find and connect to the PostGIS backend.  Fly.io will set this environment variable automatically when you run `fly launch` and setup a postgres database.  For details on the URL format, see the [dj-database-url docs](https://pypi.org/project/dj-database-url/#url-schema)
1. `python manage.py migrate` to run migrations and populate the database with the Egrid database
1. `python manage.py runserver` to start the server






