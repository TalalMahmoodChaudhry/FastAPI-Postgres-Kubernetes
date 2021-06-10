# Introduction 
This api was developed using python version 3.9

# Running API

## Without Docker

### Environment Variables
DATABASE_URL: postgresql database url

SECRET_KEY (Optional): for access tokens

APPLICATION_INSIGHTS_KEY (Optional): To persist logs to Azure Application Insights
with correlation of logs within each request

### Create Virtual Environment (Optional)
Creating a virtual environment is recommended.

`python -m venv env`

`.\env\Scripts\activate.bat` # Windows

`source env/bin/activate` # MacOS/Linux

### Installing dependencies
`pip install -r requirements.txt`

### Run app.py
`python -m src.app.app`

The application should now be listening on localhost:8000

swagger: localhost:8000/docs

Authenticate using following details:
```
username: talal
password: secret
```


## With Docker
`make clean_run`

The application should now be listening on localhost:8000

swagger: http://localhost:8000/docs

redoc: http://localhost:8000/redoc

pgadmin: http://localhost:5050

### Stopping Docker
`make destroy`

# Running Tests
`make clean_test`

# Deploying the API in Kubernetes
The deployment folder contains yaml scripts to deploy the API to Kubernetes. To run the below
command please install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl). And the docker container
needs to be pushed to the container registry and this registry url should be replaced in the
deployment/deployment.yaml file.

`kubectl apply -f deployment/ -n <namepsace> --recursive`
