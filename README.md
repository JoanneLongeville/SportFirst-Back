# SportFirst-Back

## Start with Windows

Requirements : Python3.12.0

Create Python environment :
`python -m venv venv`
`source venv/Scripts/activate`

Install dependencies:
`pip install -r requirements.txt`

Run python interpretor with terminal `py<file.py>`

## Start with Linux

Requirements : Python3.12.0

Create Python environment :
`python -m venv venv`
`source venv/bin/activate`

Install dependencies:
`pip install -r requirements.txt`

Run python interpretor with terminal `python <file.py>`

## Run the app locally

`docker compose up`
`python app/src/main.py`

## Tests

`py -v`

## Start with Docker

Build the app: `docker build -t sportfirst-back .`
Run the app: `docker run -dp 127.0.0.1:5000:5000 sportfirst-back`

Check running containers: `docker ps`
Check running and dead's containers: `docker ps -a`
Logs one container with its three first letters/numbers: `docker container logs 3a0`
Kill one container with its three first letters/numbers: `docker container stop 3a0`
Kill every containers: `docker prune`
