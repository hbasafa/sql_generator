# Introduction

This is a service for generating SQL queries from natural language questions.

# Build
```bash
docker build -t sql_generator .
```

# How to run via Docker
## Stage 1: Install dependencies
- In order to run the service, you need to have either Docker installed on your machine.

## Stage 2: Run the service
Then create a .env file in the root directory of the project by copying the .env.example file:
```bash
cp .env.example .env
```
Now change the values in the .env file to match your environment.

There are two options to run the service:
### Docker
```bash
docker run -p 9000:9000 sql_generator
```

### Docker Compose
```bash
docker-compose up -d
```

# How to run locally via Python
## Stage 1: Create virtual environment
```bash
pip install virtualenv
virtualenv env
source venv/bin/activate
```
## Stage 2: Install dependencies
```bash
pip install -r requirements.txt
```
## Stage 3: Run the service
```bash
python -m src.app.main
```


# Testing
### Test the service
```bash
curl -X POST "http://localhost:9000/generate_sql/" -H "Content-Type: application/json" -d '{"question": "Get all user emails"}'
# {"sql_query":"SELECT email FROM users;","summary":"This query retrieves all user emails from the users table."}
```

# Relative Information
### Docker images
- semitechnologies/transformers-inference:sentence-transformers-all-MiniLM-L6-v2-1.8.5
- python:3.12-slim
- pytorch/torchserve:0.8.2-cpu

### Mongo
```bash
mongo --username your_username --password your_password --authenticationDatabase admin
mongoimport --db my_database --collection my_collection --file /path/to/data.json --jsonArray
docker exec mongodb mongoimport --db admin --collection weather --file /tmp/data/weather.json --username admin --password password --authenticationDatabase admin

# SELECT customer FROM mongodb.admin.sales limit 2;
# {gender=M, age=51, email=worbiduh@vowbu.cg, satisfaction=5}
# select * from mongodb.admin.sales limit 1;
```

### Postgres
```bash
docker exec -it postgres pgbench -i -s 1 -U test -d test
```

### Useful SQL commands
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
\du # list of roles
\l # list of databases
\dt # list of tables
```

# Extra resources
- https://github.com/oobabooga/text-generation-webui
