ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setup GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

RUN python manage.py collectstatic --noinput

# run the script to populate the database
# RUN python manage.py runscript load

EXPOSE 8000

# replace demo.wsgi with <project_name>.wsgi
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "egridserver.wsgi"]
