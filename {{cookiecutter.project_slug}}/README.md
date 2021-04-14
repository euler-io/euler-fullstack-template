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

## Requirements

* Docker
* docker-compose