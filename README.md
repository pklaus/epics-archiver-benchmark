### EPICS Archiver Benchmark

Tools to benchmark EPICS archiver software in a defined way.

Currently the following archivers can be benchmarked:

* [EPICS Archiver Appliance][]
* [Cassandra Archiver for CSS][]

The setup consists of:

* SoftIOCs serving a large amount of random walk PVs implemented with `calc` records.
* The archiver software.
* (Optional) An intermediate CA Gatway application between the IOCs and the archiver.

After starting the software components, the archivers need to be configured
to archive the desired PVs. Python scripts named `register_pvs.*.py` help to
fulfil this task.

[EPICS Archiver Appliance]: https://slacmshankar.github.io/epicsarchiver_docs/
[Cassandra Archiver for CSS]: https://oss.aquenos.com/epics/cassandra-archiver/
