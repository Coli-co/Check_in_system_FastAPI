#/bin/bash

docker compose build
docker compose up -d


sleep 3

python seeder/employees_seed_file.py 

