#!/bin/bash -ex

#./render-templates.sh
# no only selected:
j2 docker-compose.jinja2.yml > docker-compose.yml

# make sure the YAML is valid...
python -c 'import yaml, sys; yaml.safe_load(sys.stdin)' < docker-compose.yml

docker-compose up --remove-orphans -d
