#!/bin/bash -ex

j2 docker-compose.jinja2.yml > docker-compose.yml
python -c 'import yaml, sys; yaml.safe_load(sys.stdin)' < docker-compose.yml

docker-compose down
