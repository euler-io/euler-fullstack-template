# {{cookiecutter.project_name}}

## How to start the development enviroment

Go to the root of your project and run:
```bash
./start-dev.sh
```

After the logs stopped rolling the following must be running:

* FastAPI docs at http://localhost:8000/docs
* FastAPI redocs at http://localhost:8000/redoc
* Elasticsearch at https://localhost:9200 (User/Pass: admin/admin with self-signed certificate)
* Kibana at http://localhost:5601 (User/Pass: admin/admin)
* Search UI at http://localhost:3000 (User/Pass: admin/admin)
* Euler API at http://localhost:8080 (User/Pass: admin/admin)

## Deploy

Go to the deploy directory and run:
```bash
./deploy.sh <deployment files output directory>
```

To start the deployment stack go to the output directory and run:
```bash
docker stack deploy -c docker-compose.yml {{ cookiecutter.project_slug }}
```
After the logs stopped rolling the following must be running:

* FastAPI docs at https://<server-name\>/search/api/docs
* FastAPI redocs at https://<server-name\>/search/api/redoc
* Kibana at https://<server-name\>/kibana
* Search UI at https://<server-name\>/search/app


## Requirements

* Docker
* docker-compose