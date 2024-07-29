# Alert aggregation service

## Description

Tool for merging alerts from different environments and sending them, to the mattermost or slack by webhook url.

## Purpose

Making merging all messages from some scripts in different environments and sending them to the mattermost or slack easier 

## Usage

### Curl examples 

1) Create alert

```
curl --header "Content-Type: application/json" --request POST --data '{"name":"Alert name","message":"Alert message", "env": "environment1"}' http://localhost:8000/api/v1/alert/create
```

2) Send alerts to mattermost or slack
   
```
curl --header "Content-Type: application/json" --request POST http://localhost:8000/api/v1/alert/send/{environment}
```

3) List all alerts in specifiv environment
   
```
curl -X 'GET' 'http://0.0.0.0:8000/api/v1/alert/list/{environment}' -H 'accept: application/json'
```

4) Clear all alerts for specific environment

```
curl -X 'DELETE' 'http://0.0.0.0:8000/api/v1/alert/clear/{environment}' -H 'accept: application/json'
```

### Run with docker-compose.yaml

1) Change `MATTERMOST_WEBHOOK_URL` environment variable to channel webhook url
2) Change `ENVIRONMENTS` environment variable to list of alerts environments in format `env1 env2 ... envN`
3) Run docker-compose.yaml: `docker-compose up -d`
4) Your alerts will be mapping into `./data` directory

### Logs

For viewing logs use `docker logs {container-id}` command