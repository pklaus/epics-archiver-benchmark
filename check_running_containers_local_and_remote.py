#!/usr/bin/env python

import docker

client_local = docker.from_env()
client_ssh = docker.APIClient(base_url='ssh://192.168.2.2')

print(client_local.version())
print(client_ssh.version())

print(client_local.containers.list())
print(client_ssh.containers.list())
