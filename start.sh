#/bin/bash

docker compose build
docker compose up -d


export PYTHONPATH=$PWD

sleep 3

python seeder/employees_seed_file.py 

