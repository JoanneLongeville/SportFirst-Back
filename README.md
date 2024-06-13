# SportFirst-Back

## Start with Docker

``docker build -t sportfirst-back .``

``docker compose up``

## Start with Windows

Requirements : Python3.12.0

Create Python environment :

    python -m venv venv
    venv/Scripts/activate

Install dependencies:

    pip install -r requirements.txt

Run python interpretor with terminal ``py<file.py>``

## Start with Linux

Requirements : Python3.12.0

Create Python environment :

    python -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run python interpretor with terminal ``python <file.py>``

``docker ps`` to check if PostgreSQL is running.

``docker exec -it sportfirst-back-db-1 psql -U postgres -d sportfirst``
