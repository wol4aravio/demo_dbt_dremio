FROM python:3.8.6-slim

RUN apt-get update
RUN apt-get install -y \
    git \
    lsb-release \
    apt-transport-https \
    ca-certificates \
    wget \
    unixodbc \
    unixodbc-dev \
    alien

RUN wget https://download.dremio.com/odbc-driver/1.5.1.1001/dremio-odbc-1.5.1.1001-1.x86_64.rpm
RUN alien -i dremio-odbc-1.5.1.1001-1.x86_64.rpm

RUN pip3 install poetry

WORKDIR /demo_dbt_dremio
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

COPY demo_dbt_dremio demo_dbt_dremio
COPY fill.py .
RUN poetry install --no-dev

ENTRYPOINT [ "poetry", "run"]
