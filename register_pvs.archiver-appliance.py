#!/usr/bin/env python

import requests, typing, time

PVs = [
    f"IOC{ioc}:{slice}:{pv}:x"
    for ioc in range(1, 26)
    #for slice in (0, 1)
    for slice in (0, )
    for pv in range(10000)
]


# reverse order...
#PVs = list(reversed(PVs))

#PVs = [
#   "IOC0:3:267:x",
#   "IOC0:3:268:x",
#   "IOC0:3:269:x",
#  ...
#]

# ----

def register_pvs(
        pvs: typing.List[str],
        samplingperiod: float = None,
        samplingmethod: str = None,
        policy: str = None,
        server: str = "http://10.2.99.1:17665",
        ret_status: bool = True,
        ):
    # ?pv={url_pv_list}&samplingperiod=0.1&samplingmethod=MONITOR&policy=2HzPVs
    params = {"pv": ",".join(pvs)}
    if samplingperiod:
        params["samplingperiod"] = samplingperiod
    if samplingmethod:
        params["samplingmethod"] = samplingmethod
    if policy:
        params["policy"] = policy
    
    r = requests.get(f"{server}/mgmt/bpl/archivePV", params=params)
    assert r.status_code == 200
    params = {"pv": ",".join(pvs)}
    if ret_status:
        r = requests.get(f"{server}/mgmt/bpl/getPVStatus", params=params)
        assert r.status_code == 200
        return r.json()

# ----

chunk_size = 200
start = time.time()
last = start
for chunk_idx in range(0, len(PVs), chunk_size):
    pv_chunk = PVs[chunk_idx:chunk_idx + chunk_size]
    url_pv_list = ','.join(pv_chunk).replace(':', '%3A')
    status = register_pvs(pv_chunk, samplingperiod=0.1, samplingmethod="MONITOR", policy="2HzPVs")
    print(f"{time.time()-start:.1f} s [Δ = {time.time()-last:.3f} s] - Added PVs {status[0]['pvName']} .. {status[-1]['pvName']} (status: '{status[0]['status']}'/'{status[-1]['status']}' resp).")
    last = time.time()

