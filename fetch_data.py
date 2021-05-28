#!/usr/bin/env python

import requests
import time
import json

SLOWDOWN=0

while True:
    for filename, url in [
            ("metrics_gen.jsonl", "http://10.2.99.1:17665/mgmt/bpl/getApplianceMetrics"),
            ("metrics_det.jsonl", "http://10.2.99.1:17665/mgmt/bpl/getApplianceMetricsForAppliance?appliance=appliance0"),
            ("metrics_mem.jsonl", "http://10.2.99.1:17665/mgmt/bpl/getProcessMetricsDataForAppliance?appliance=appliance0"),
        ]:
        start = time.time()
        r = requests.get(url)
        duration = time.time() - start
        data = r.json()
        with open(filename, "at") as f:
            f.write(json.dumps({'start': start, 'duration': duration, 'data': data}) + "\n")
    time.sleep(1 + SLOWDOWN)
