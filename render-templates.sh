#!/bin/bash -ex

# https://github.com/kolypto/j2cli

## one time action:
# pip install j2cli[yaml] pyyaml
# sudo pacman -S yamllint

j2 docker-compose.jinja2.yml > docker-compose.yml
python -c 'import yaml, sys; yaml.safe_load(sys.stdin)' < docker-compose.yml
#yamllint docker-compose.yml # <- tooo strict!

j2 all_pvs.archiver-appliance.jinja2.xml > all_pvs.archiver-appliance.xml
xmllint --valid --noout all_pvs.archiver-appliance.xml

j2 all_pvs.cassandra-pv-archiver.jinja2.xml > all_pvs.cassandra-pv-archiver.xml
# takes ages...
#xmllint --noout --schema /home/pklaus/phd/projects/epics/docker-cassandra-pv-archiver/example-deployment/cassandra-pv-archiver-configuration-3.0.0.xsd  all_pvs.cassandra-pv-archiver.xml
