#!/usr/bin/env python

import typing, requests, json, time


def register_pvs(
    pvs: typing.List[str],
    server: str = "http://localhost:4812",
    server_id: str = "e80a4eae-ba67-4826-823c-51839898275c",
    ret_status: bool = True,
):
    """
    Uses the JSON Admin Interface
    https://oss.aquenos.com/cassandra-pv-archiver/docs/3.2.6/manual/htmlsingle/#admin_api.run_archive_configuration_commands
    """

    data = {"commands": []}
    for pv in pvs:
        data["commands"].append(
            {
                "channelName": pv,
                "commandType": "add_or_update_channel",
                "controlSystemType": "channel_access",
                "enabled": True,
                "serverId": server_id,
            }
        )

    r = requests.post(
        f"{server}/admin/api/1.0/run-archive-configuration-commands",
        auth=("admin", "admin"),
        json=data,
    )
    assert r.status_code == 200, r.status_code
    return r.json()


# ----

PVs = [
    f"IOC{ioc}:{slice}:{pv}:x"
    for ioc in range(25)
    for slice in (0,)
    for pv in range(10000)
]

chunk_size = 100
start = time.time()
last = start
for chunk_idx in range(0, len(PVs), chunk_size):
    pv_chunk = PVs[chunk_idx : chunk_idx + chunk_size]
    url_pv_list = ",".join(pv_chunk).replace(":", "%3A")
    response = register_pvs(pv_chunk)
    assert all(result["success"] == True for result in response["results"])
    # print(response)
    print(f"{time.time()-start:.1f} s [Δ = {time.time()-last:.3f} s] - Added PVs {pv_chunk[0]} .. {pv_chunk[-1]}")
    last = time.time()
