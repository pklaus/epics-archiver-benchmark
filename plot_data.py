#!/usr/bin/env python

import json, argparse
from datetime import datetime, timezone
# external:
import dateparser
from matplotlib import pyplot as plt

def dateutil_parse_local(point_in_time: str):
    dt = dateparser.parse(point_in_time)
    return dt

def dateutil_parse_utc(point_in_time: str):
    dt = dateparser.parse(point_in_time, settings={'TIMEZONE': 'UTC'})
    return dt.replace(tzinfo=timezone.utc)

# general metrics
GEN = []
with open("metrics_gen.jsonl", "rt") as f:
    for line in f.readlines():
        GEN.append(json.loads(line))
        # example chunk:
        #{'data': [{'capacityUtilized': 'N/A',
        #           'connectedPVCount': '27112',
        #           'dataRate': '586,518.88',
        #           'dataRateGBPerDay': '47.19',
        #           'dataRateGBPerYear': '17,226.17',
        #           'disconnectedPVCount': '9470',
        #           'eventRate': '28,665.56',
        #           'formattedWriteThreadSeconds': '0.49',
        #           'instance': 'appliance0',
        #           'maxETLPercentage': '0',
        #           'pvCount': '36582',
        #           'secondsConsumedByWritter': '0.48627441860465126',
        #           'status': 'Working',
        #           'timeForOverallETLInSeconds(0)': '0',
        #           'timeForOverallETLInSeconds(1)': '0',
        #           'totalETLRuns(0)': '0',
        #           'totalETLRuns(1)': '0'}],
        # 'duration': 0.028889894485473633,
        # 'start': 1601028901.436821}

# detailed metrics
DET = []
with open("metrics_det.jsonl", "rt") as f:
    for line in f.readlines():
        DET.append(json.loads(line))
        #{'data': [{'name': 'Appliance Identity',
        #           'source': 'mgmt',
        #           'value': 'appliance0'},
        #          {'name': 'Total PV count', 'source': 'engine', 'value': '2103'},
        #          {'name': 'Disconnected PV count', 'source': 'engine', 'value': '0'},
        #          {'name': 'Connected PV count', 'source': 'engine', 'value': '2103'},
        #          {'name': 'Paused PV count', 'source': 'engine', 'value': '0'},
        #          {'name': 'Total channels', 'source': 'engine', 'value': '16824'},
        #          {'name': 'Approx pending jobs in engine queue',
        #           'source': 'engine',
        #           'value': '1'},
        #          {'name': 'Event Rate (in events/sec)',
        #           'source': 'engine',
        #           'value': '2,093.91'},
        #          {'name': 'Data Rate (in bytes/sec)',
        #           'source': 'engine',
        #           'value': '46,975.96'},
        #          {'name': 'Data Rate in (GB/day)',
        #           'source': 'engine',
        #           'value': '3.78'},
        #          {'name': 'Data Rate in (GB/year)',
        #           'source': 'engine',
        #           'value': '1,379.69'},
        #          {'name': 'Time consumed for writing samplebuffers to STS (in secs)',
        #           'source': 'engine',
        #           'value': '0.1'},
        #          {'name': 'Benchmark - writing at (events/sec)',
        #           'source': 'engine',
        #           'value': '216,425.2'},
        #          {'name': 'Benchmark - writing at (MB/sec)',
        #           'source': 'engine',
        #           'value': '4.63'},
        #          {'name': 'PVs pending computation of meta info',
        #           'source': 'engine',
        #           'value': '0'},
        #          {'name': 'Total number of reference counted channels',
        #           'source': 'engine',
        #           'value': '2103'},
        #          {'name': 'Total number of CAJ channels',
        #           'source': 'engine',
        #           'value': '2103'},
        #          {'name': 'Channels with pending search requests',
        #           'source': 'engine',
        #           'value': '0 of 2103'},
        #          {'name': 'PVs in archive workflow',
        #           'source': 'mgmt',
        #           'value': '18753'},
        #          {'name': 'Capacity planning last update',
        #           'source': 'mgmt',
        #           'value': 'Sep/25/2020 10:41:38 +00:00'},
        #          {'name': 'Engine write thread usage', 'source': 'mgmt', 'value': '0'},
        #          {'name': 'Aggregated appliance storage rate (in GB/year)',
        #           'source': 'mgmt',
        #           'value': '5,950.75'},
        #          {'name': 'Aggregated appliance event rate (in events/sec)',
        #           'source': 'mgmt',
        #           'value': '10,129.47'},
        #          {'name': 'Aggregated appliance PV count',
        #           'source': 'mgmt',
        #           'value': '10,000'},
        #          {'name': 'Incremental appliance storage rate (in GB/year)',
        #           'source': 'mgmt',
        #           'value': '5,950.75'},
        #          {'name': 'Incremental appliance event rate (in events/sec)',
        #           'source': 'mgmt',
        #           'value': '10,129.47'},
        #          {'name': 'Incremental appliance PV count',
        #           'source': 'mgmt',
        #           'value': '10,000'}],
        # 'duration': 0.0041654109954833984,
        # 'start': 1601031014.5272684}

# memory metrics
MEM = []
with open("metrics_mem.jsonl", "rt") as f:
    for line in f.readlines():
        MEM.append(json.loads(line))
        #{'data': [{'data': [[1601198632000, 2.54],
        #                    [1601203852000, 18.47],
        #                    [1601203912000, 17.61]],
        #           'label': 'system_load (%)'},
        #          {'data': [[1601198632000, 5.784291436430067],
        #                    [1601198993000, 35.940306703560054],
        #                    [1601203912000, 23.69133603060618]],
        #           'label': 'engine_heap (%)'},
        #          {'data': [[1601198633000, 5.833119561430067],
        #                    [1601198933000, 24.62394153699279],
        #                    [1601203913000, 27.25578915560618]],
        #           'label': 'etl_heap (%)'},
        #          {'data': [[1601198635000, 5.881947686430067],
        #                    [1601198695000, 16.95973655441776],
        #                    [1601203915000, 21.66814556112513]],
        #           'label': 'retrieval_heap (%)'}],
        # 'duration': 0.0038259029388427734,
        # 'start': 1601203959.5360134}

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', '-s', type=dateutil_parse_local)
    parser.add_argument('--end', '-e', type=dateutil_parse_local)
    return parser.parse_args()

args = get_args()

def filter_start_end(ds, start=None, end=None):
    if args.start:
        ds = [chunk for chunk in ds if chunk["start"] > args.start.timestamp()]
    if args.end:
        ds = [chunk for chunk in ds if chunk["start"] < args.end.timestamp()]
    return ds

def convert_start_to_datetime(ds):
    for chunk in ds:
        #chunk["start"] = datetime.utcfromtimestamp(chunk["start"])
        chunk["start"] = datetime.fromtimestamp(chunk["start"])
    return ds

GEN = convert_start_to_datetime(filter_start_end(GEN, args.start, args.end))
DET = convert_start_to_datetime(filter_start_end(DET, args.start, args.end))
MEM = convert_start_to_datetime(filter_start_end(MEM, args.start, args.end))

plots = [
  {
      'slug': 'duration-vs-time',
      'title': 'duration plottet against date/time',
      'method': 'plot',
      'x': lambda chunk: chunk["start"],
      'y': lambda chunk: chunk["duration"],
  },
  {
      'slug': 'disconnectedPVCount-vs-totalPVcount',
      'method': 'scatter',
      'x': lambda chunk: int(chunk["data"][0]["pvCount"]),
      'y': lambda chunk: int(chunk["data"][0]["disconnectedPVCount"]),
  },
  {
      'slug': 'secondsConsumedByWritter-vs-connectedPVCount',
      'x': lambda chunk: int(chunk["data"][0]["connectedPVCount"]),
      'y': lambda chunk: flt(chunk["data"][0]["secondsConsumedByWritter"]),
  },
  {
      'slug': 'secondsConsumedByWritter-vs-eventRate',
      'x': lambda chunk: flt(chunk["data"][0]["eventRate"]),
      'y': lambda chunk: flt(chunk["data"][0]["secondsConsumedByWritter"]),
  },
  {
      'slug': 'connectedPVCount-vs-start',
      'x': lambda chunk: chunk["start"],
      'y': lambda chunk: int(chunk["data"][0]["connectedPVCount"]),
  },
  {
      'slug': 'secondsConsumedByWritter-vs-start',
      'x': lambda chunk: chunk["start"],
      'y': lambda chunk: flt(chunk["data"][0]["secondsConsumedByWritter"]),
  },
  {
      'slug': 'dataRate-vs-connectedPVCount',
      'method': 'scatter',
      'method_kwargs': {'s': 0.4},
      'x': lambda chunk: int(chunk["data"][0]["connectedPVCount"]),
      'y': lambda chunk: flt(chunk["data"][0]["dataRate"]),
  },
  {
      'slug': "benchmarkEventsPerS-vs-start",
      'data': DET,
      'x': lambda chunk: chunk["start"],
      'y': lambda chunk: flt(choose(chunk["data"], "Benchmark - writing at (events/sec)", "nan")),
  },
  {
      'slug': "pvs-in-archive-workflow--vs--start",
      'data': DET,
      'method': 'scatter',
      'method_kwargs': {'s': 0.4},
      'x': lambda chunk: chunk["start"],
      'y': lambda chunk: int(choose(chunk["data"], "PVs in archive workflow")),
  },
  {
      'slug': "pending-vs-start",
      'data': DET,
      'method': 'scatter',
      'method_kwargs': {'s': 0.4},
      'x': lambda chunk: chunk["start"],
      'y': lambda chunk: int(choose(chunk["data"], "Channels with pending search requests", "0 of 0").partition(" of ")[0]),
  },
  {
      'slug': "pending-vs-total",
      'data': DET,
      'method': 'scatter',
      'method_kwargs': {'s': 0.4},
      'x': lambda chunk: int(choose(chunk["data"], "Channels with pending search requests", "0 of 0").partition(" of ")[2]),
      'y': lambda chunk: int(choose(chunk["data"], "Channels with pending search requests", "0 of 0").partition(" of ")[0]),
  },
  {
      'slug': "system_load",
      'data': MEM,
      'x': lambda chunk: datetime.fromtimestamp(first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "system_load (%)", lambda x: x["data"][-1][0])/1000),
      'y': lambda chunk: first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "system_load (%)", lambda x: x["data"][-1][1]),
  },
  {
      'slug': "engine_heap",
      'data': MEM,
      'x': lambda chunk: datetime.fromtimestamp(first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "engine_heap (%)", lambda x: x["data"][-1][0])/1000),
      'y': lambda chunk: first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "engine_heap (%)", lambda x: x["data"][-1][1]),
  },
  {
      'slug': "etl_heap",
      'data': MEM,
      'x': lambda chunk: datetime.fromtimestamp(first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "etl_heap (%)", lambda x: x["data"][-1][0])/1000),
      'y': lambda chunk: first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "etl_heap (%)", lambda x: x["data"][-1][1]),
  },
  {
      'slug': "retrieval_heap",
      'data': MEM,
      'x': lambda chunk: datetime.fromtimestamp(first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "retrieval_heap (%)", lambda x: x["data"][-1][0])/1000),
      'y': lambda chunk: first_matching_from_iterable(chunk["data"], lambda x: x["label"] == "retrieval_heap (%)", lambda x: x["data"][-1][1]),
  },

]

def flt(val):
    return float(val.replace(",", ""))

def first_matching_from_iterable(candidates, match_func, extract_func=None):
    for candidate in candidates:
        if match_func(candidate):
            # we found our match
            if extract_func:
                return extract_func(candidate)
            else:
                return candidate
    raise ValueError("No match found")

def choose(iterable, name, if_not_found=None):
    try:
        return first_matching_from_iterable(iterable, lambda x: x["name"] == name, lambda x: x["value"])
    except ValueError:
        return if_not_found

for plot in plots:
    print(plot.get("title", plot.get("slug")))
    # we have the following data sources: GEN, DET, MEM; default is GEN
    data = plot.get("data", GEN)
    x = [plot["x"](chunk) for chunk in data]
    y = [plot["y"](chunk) for chunk in data]
    plt.figure(figsize=(10, 6))
    plt.title(plot.get("title", plot.get("slug")))
    method = plot.get("method", "plot")
    getattr(plt, method)(x, y, **plot.get("method_kwargs", {}))
    plt.savefig(f"plots/{plot['slug']}.png", dpi=200)
    plt.show()
