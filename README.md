# SportFirst-Back

# Start with Docker 

docker build -t sportfirst-back .
docker compose up

# Start with Windows

Python3.12.0

Create Python environment : 

    python -m venv venv
    venv/Scripts/activate
    pip install poetry

Install dependencies: 

    cd venv
    pip install -r requirements.txt

Run python interpretor with terminal ``py<file.py>``



``docker ps`` to check if PostgreSQL is running.

``docker exec -it sportfirst-back-db-1 psql -U postgres -d sportfirst``