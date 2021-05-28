#!/usr/bin/env python

"""
pip install "docker[ssh]"
pip install paramiko[all]
"""

import time, os
import docker
from colorama import Fore
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

#client_hades = docker.from_env()
#client_hades= docker.DockerClient(base_url='unix://var/run/docker.sock')
#client_hades = docker.DockerClient(base_url='ssh://192.168.2.1:22')
#client_owl = docker.DockerClient(base_url='ssh://10.2.1.52:22')
client_usb_arch = docker.DockerClient(base_url='ssh://10.2.1.24:22')
#client_owl = docker.DockerClient(base_url='ssh://owl:22')

client_iocs = client_usb_arch

#print(client_hades.version())
#print(client_owl.version())
#print([client_hades.containers.list(all=True)])

def cleanup():
    """ remove existing networks and container """
    for container in client_iocs.containers.list(all=True):
        print(f"removing container {container.name}")
        try:
            container.stop(timeout=5)
        except Exception as e:
            print(e)
        try:
            container.remove()
        except Exception as e:
            print(e)
    for net in client_iocs.networks.list():
        if net.name in ("epics_field", "epics_a_supervisory"):
            print(f"removing network {net.name}")
            try:
                net.remove()
            except Exception as e:
                print(e)

cleanup()

time.sleep(1)

field_net = client_iocs.networks.create(
    "epics_field",
    #driver="bridge",
    #driver="macvlan", options={"parent": "enp5s0"},
    driver="macvlan", options={"parent": "eno1"},
    ipam=docker.types.IPAMConfig(
        pool_configs=[
            docker.types.IPAMPool(
                #subnet="10.3.0.0/16",
                subnet="10.2.0.0/16",
                #gateway="172.20.0.1",
            )
        ]
    )
)
#supervisory_net = client_iocs.networks.create(
#    "epics_a_supervisory",
#    #driver="bridge",
#    driver="macvlan", options={'parent': 'enp5s0'},
#    ipam=docker.types.IPAMConfig(
#        pool_configs=[
#            docker.types.IPAMPool(
#                subnet="192.168.2.0/24",
#                #gateway="192.168.2.1",
#                #subnet="10.10.0.0/16",
#                #gateway="10.10.0.1",
#            )
#        ]
#    )
#)

ALL_CONTAINERS = []


comment = """
# start CA Gateway
print("Creating the CA Gateway container.")
ca_gateway = client_iocs.containers.create(
    #"pklaus/ca-gateway",
    #"-sip 10.10.2.2 -cip 172.20.255.255 -pvlist /pvlist -access /access -log /dev/stdout -debug 1",
    "pklaus/ca-gateway:1.0",
    "/epics/ca-gateway/bin/linux-x86_64/gateway -sip 192.168.2.5 -cip 172.20.255.255 -pvlist /pvlist -access /access -log /dev/stdout -debug 0",
    environment=[],
    name="ca-gateway",
    #restart_policy={"Name": "on-failure", "MaximumRetryCount": 5},
    detach=True,
    #auto_remove=True,
    network="none",
    #network_mode="host",
    ports = {
        #'5064/tcp': ('10.2.1.28', 5064),
        #'5065/udp': ('10.2.1.28', 5065),
        '5064/tcp': 5064,
        '5065/udp': 5065,
    },
    volumes = {
        os.path.abspath('./gw_access'): {'bind': '/access', 'mode': 'ro'},
        os.path.abspath('./gw_pvlist'): {'bind': '/pvlist', 'mode': 'ro'},
    },

)
ALL_CONTAINERS.append(ca_gateway)

client_iocs.networks.get("none").disconnect(ca_gateway)
#supervisory_net.connect(ca_gateway, ipv4_address="10.10.2.2")
supervisory_net.connect(ca_gateway, ipv4_address="192.168.2.5")
field_net.connect(ca_gateway, ipv4_address="172.20.255.254")

ca_gateway.start()
"""

for i in range(1, 26):
    print(f"Creating and running the IOC container {i}.")
    ioc = client_iocs.containers.create(
        #"slominskir/softioc:latest",
        "pklaus/epics_base:7.0.4_debian",
        # --
        f"softIoc -m DEVICE=IOC{i}:1 -m DEVICE=IOC{i}:0 -d /db/10000_random.db",
        #"echo hello world",
        environment=["MAX_SLICE=9999"],
        auto_remove=True,
        #remove=True,
        name=f"massive-ioc-{i:02d}",
        detach=True,
        #restart_policy={"Name": "on-failure", "MaximumRetryCount": 5},
        stdin_open=True,
        tty=True,
        volumes = {
            os.path.abspath('./epics_db/'): {'bind': '/db', 'mode': 'ro'},
        },
        #network=field_net.name,
        network="none",
        #network_mode="host",
        #ports = {
        #    '5064/tcp': 5064,
        #    '5065/udp': 5065,
        #},
    )
    #ipv4_address = '10.3.100.' + str(i)
    ipv4_address = '10.2.100.' + str(i)
    logger.info(f"connecting the desired (macvlan) network with a pre-determined IP {ipv4_address}")
    client_iocs.networks.get("none").disconnect(ioc)
    #supervisory_net.connect(ioc, ipv4_address='192.168.2.' + str(200 + i))
    field_net.connect(ioc, ipv4_address=ipv4_address)
    logger.info("starting the IOC")
    ioc.start()
    ALL_CONTAINERS.append(ioc)


#print(ca_gateway.logs().decode('utf-8'))

for container in ALL_CONTAINERS:
    container.last = 1

sys.exit(0)

try:
    while True:
        for container in ALL_CONTAINERS:
            #dkg = container.logs(stream=True, timestamps=True, follow=False)
            now = time.time()
            output = container.logs(stream=False, timestamps=True, follow=False, since=container.last)
            container.last = int(now)
            output = output.decode("utf-8")
            if not output:
                continue
            for line in output.split("\n"):
                print(Fore.CYAN + container.name, Fore.YELLOW + line)
            time.sleep(0.1)
except KeyboardInterrupt:
    print("Ctrl-c was hit. Exiting.")
    pass
finally:
    print("finally")
    cleanup()
